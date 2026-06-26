# 📊 Statify 2.0 — GenAI Financial Analyst Chatbot

> **Week 1 Project** | Statify 2.0 Programme

## 🧠 What It Does

Statify is an LLM-powered financial analyst chatbot that:
- Retrieves **live stock prices** and key metrics (price, P/E, market cap, 52-week range) via **yfinance**.
- Aggregates **latest financial news** and market sentiment via **DuckDuckGo Search**.
- Uses a **Hugging Face open-source LLM** (Mistral-7B-Instruct by default) to reason over tool outputs and deliver conversational, data-backed answers.

---

## 🏗️ Architecture Overview

```
Week1.py  (entry point & chat loop)
    │
    ├── Loads .env (HF_TOKEN, HF_MODEL_ID)
    ├── Initialises HuggingFaceEndpoint LLM
    ├── Builds a ReAct Agent (LangChain create_react_agent)
    │       │
    │       ├── tool.py ──► get_stock_price(ticker)
    │       │                   └─ yfinance.Ticker → StockPriceOutput (schema.py)
    │       │
    │       └── tool.py ──► search_news(query, max_results)
    │                           └─ DuckDuckGo DDGS.news() → NewsSearchOutput (schema.py)
    │
    └── AgentExecutor runs the Reason → Act → Observe loop
            └─ Returns Final Answer to the CLI chat loop
```

### File Responsibilities

| File | Responsibility |
|------|---------------|
| `Week1.py` | App entry point. Loads env, builds the ReAct agent, runs the CLI chat loop. |
| `tool.py` | All LangChain `@tool` definitions — stock price fetcher and news searcher. |
| `schema.py` | Pydantic models for tool inputs/outputs and the top-level `AgentResponse`. |
| `.env.example` | Template for required environment variables. |
| `requirements.txt` | Python dependency list. |

---

## ⚙️ Setup & Running Locally

### 1. Prerequisites

- Python **3.10+**
- A free [Hugging Face account](https://huggingface.co/join) with an API token that has **Inference API** access.

### 2. Clone the repository

```bash
git clone https://github.com/24WH1A0586/STATIFY_2.0_<YourTeamName>.git
cd STATIFY_2.0_Rangers
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Optional — change the model if desired
HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.3
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 6. Run the chatbot

```bash
python Week1.py
```

You should see:

```
⏳  Loading model: mistralai/Mistral-7B-Instruct-v0.3 …
✅  Statify Financial Analyst is ready!

╔══════════════════════════════════════════════════════╗
║   📊  STATIFY 2.0 — AI Financial Analyst Chatbot     ║
╚══════════════════════════════════════════════════════╝

You:
```

---

## 💬 Example Queries

```
What is the current price of Apple stock?
Give me the latest news about Tesla.
Analyse Microsoft — price, valuation, and any recent headlines.
What is NVIDIA's P/E ratio and 52-week range?
```

---

## 🔑 Supported Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HF_TOKEN` | ✅ Yes | — | Your Hugging Face API token |
| `HF_MODEL_ID` | No | `mistralai/Mistral-7B-Instruct-v0.3` | HF model to use as the LLM engine |

---

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `langchain` | Agent orchestration & ReAct framework |
| `langchain-huggingface` | HuggingFaceEndpoint LLM wrapper |
| `huggingface-hub` | Model access via Inference API |
| `yfinance` | Real-time stock data |
| `duckduckgo-search` | Live news aggregation |
| `pydantic` | Schema validation |
| `python-dotenv` | `.env` file loading |

---

## 🛡️ Security Notes

- API keys live only in your local `.env` file which is git-ignored.
- The `.env.example` shows only placeholder values — safe to commit.
- yfinance makes unauthenticated public requests; no key required.
- DuckDuckGo search requires no API key.
