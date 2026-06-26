"""
Week1.py — Entry point for the Statify 2.0 GenAI Financial Analyst Chatbot.

Architecture:
  - LLM         : Hugging Face open-source model (via HuggingFaceEndpoint)
  - Tools       : get_stock_price + search_news (defined in tool.py)
  - Agent type  : ReAct (Reason + Act) via LangChain
  - Validation  : Pydantic schemas (schema.py)
  - Interface   : Interactive CLI loop
"""

import os
import sys
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from tool import TOOLS

# ── Environment ────────────────────────────────────────────────────────────────

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID  = os.getenv("HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.3")

if not HF_TOKEN:
    sys.exit(
        "\n[ERROR] HF_TOKEN not found.\n"
        "  1. Copy .env.example to .env\n"
        "  2. Paste your Hugging Face token into HF_TOKEN=\n"
        "  3. Re-run: python Week1.py\n"
    )

# ── System Prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Statify, an expert AI financial analyst assistant.
You have access to real-time stock data and live financial news tools.
Your job is to answer the user's questions accurately, using the tools when needed.

Always:
- Use get_stock_price when asked about a stock's price, valuation, or metrics.
- Use search_news when asked about recent news, market sentiment, or analyst views.
- Be concise, professional, and cite the data you retrieved.
- If a ticker is ambiguous, ask the user to clarify.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

# ── Agent Setup ────────────────────────────────────────────────────────────────

def build_agent() -> AgentExecutor:
    """Initialise the Hugging Face LLM and wire up the ReAct agent."""
    print(f"⏳  Loading model: {MODEL_ID} …")

    llm = HuggingFaceEndpoint(
        repo_id=MODEL_ID,
        huggingfacehub_api_token=HF_TOKEN,
        temperature=0.1,
        max_new_tokens=1024,
        task="text-generation",
    )

    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
    agent  = create_react_agent(llm=llm, tools=TOOLS, prompt=prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,          # set False to hide chain-of-thought in production
        max_iterations=6,
        handle_parsing_errors=True,
        return_intermediate_steps=False,
    )

    print("✅  Statify Financial Analyst is ready!\n")
    return executor


# ── CLI Chat Loop ──────────────────────────────────────────────────────────────

def chat_loop(executor: AgentExecutor) -> None:
    """Run an interactive terminal conversation with the agent."""
    chat_history: list = []

    BANNER = """
╔══════════════════════════════════════════════════════╗
║   📊  STATIFY 2.0 — AI Financial Analyst Chatbot    ║
║   Type 'exit' or 'quit' to end the session.         ║
╚══════════════════════════════════════════════════════╝
"""
    print(BANNER)
    print("Examples:")
    print("  • What is the current stock price of Apple?")
    print("  • Show me the latest news about Tesla.")
    print("  • Give me a full analysis of Microsoft (MSFT).\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! 👋")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Goodbye! 👋")
            break

        # Build conversation context
        history_str = ""
        for msg in chat_history[-6:]:   # keep last 3 turns for context
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            history_str += f"{role}: {msg.content}\n"

        full_input = f"{history_str}User: {user_input}" if history_str else user_input

        try:
            response = executor.invoke({"input": full_input})
            answer   = response.get("output", "I'm sorry, I couldn't generate a response.")

            print(f"\n🤖 Statify: {answer}\n")
            print("-" * 60)

            # Save turn to history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=answer))

        except Exception as e:
            print(f"\n[Error] {e}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent_executor = build_agent()
    chat_loop(agent_executor)
