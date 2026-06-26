"""
Week1.py — Entry point for the Statify 2.0 GenAI Financial Analyst Chatbot.

Architecture:
  - LLM         : Groq (llama-3.3-70b-versatile) via langchain-groq
  - Tools       : get_stock_price + search_news (defined in tool.py)
  - Agent type  : ReAct (Reason + Act) via LangChain
  - Validation  : Pydantic schemas (schema.py)
  - Interface   : Interactive CLI loop
"""

import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from tool import TOOLS

# ── Environment ────────────────────────────────────────────────────────────────

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID     = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    sys.exit(
        "\n[ERROR] GROQ_API_KEY not found.\n"
        "  1. Get a free key at: https://console.groq.com\n"
        "  2. Add GROQ_API_KEY=your_key to your .env file\n"
        "  3. Re-run: python3 Week1.py\n"
    )

# ── System Prompt ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Statify, an expert AI financial analyst assistant.
You have access to real-time stock data and live financial news tools.

You have access to the following tools:
{tools}

CRITICAL RULES:
- NEVER write Final Answer and Action in the same response block.
- If you need to use a tool, output ONLY Thought + Action + Action Input. Stop there.
- Only write Final Answer AFTER you have seen the Observation from the tool.
- Never fabricate Observations. Wait for the real tool output.
- For get_stock_price, Action Input must be ONLY the ticker symbol, e.g.: AAPL
- For search_news, Action Input must be ONLY the search query text, e.g.: Tesla stock news 2025
- Do NOT include parameter names like 'ticker =' or 'query =' in Action Input.

Use EXACTLY this format:

Question: the input question you must answer
Thought: what do I need to do?
Action: one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

# ── Agent Setup ────────────────────────────────────────────────────────────────

def build_agent() -> AgentExecutor:
    print(f"⏳  Loading model: {MODEL_ID} (via Groq) …")

    llm = ChatGroq(
        model=MODEL_ID,
        api_key=GROQ_API_KEY,
        temperature=0.1,
        max_tokens=1024,
    )

    prompt   = PromptTemplate.from_template(SYSTEM_PROMPT)
    agent    = create_react_agent(llm=llm, tools=TOOLS, prompt=prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=True,
        max_iterations=6,
        max_execution_time=30,
        handle_parsing_errors=True,
        return_intermediate_steps=False,
    )

    print("✅  Statify Financial Analyst is ready!\n")
    return executor


# ── CLI Chat Loop ──────────────────────────────────────────────────────────────

def chat_loop(executor: AgentExecutor) -> None:
    """Run an interactive terminal conversation with the agent."""

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

        try:
            response = executor.invoke({"input": user_input})
            answer   = response.get("output", "I'm sorry, I couldn't generate a response.")

            if "Agent stopped" in answer:
                answer = "I encountered an issue processing your request. Please try rephrasing your question."

            print(f"\n🤖 Statify: {answer}\n")
            print("-" * 60)

        except Exception as e:
            print(f"\n[Error] {e}\n")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    agent_executor = build_agent()
    chat_loop(agent_executor)