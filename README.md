# 📊 STATIFY 2.0 — AI Financial Analyst Chatbot

**Team Name:** Rangers

**Team Members:**

* CH. Charvi
* V. Sai Dhathri

---

# Overview

Statify 2.0 is an LLM-powered financial analyst chatbot that provides real-time stock prices and live market news for any company. Users interact with the chatbot through a conversational Command-Line Interface (CLI), allowing them to retrieve financial insights using natural language.

---

# Architecture

```text
                    User
                      │
                      ▼
                 Week1.py
                      │
                      ▼
        LLM (Meta Llama 3.3 70B via Groq)
                      │
                      ▼
          ReAct Agent (LangChain)
             /                 \
            ▼                   ▼
   get_stock_price         search_news
      (yfinance)         (DuckDuckGo Search)
             \                 /
              └──── schema.py ────┘
             (Pydantic Validation)
```

**Week1.py** is the entry point of the application. It initializes the LLM, connects it with the available tools, and starts the interactive chatbot.

**tool.py** defines two LangChain-compatible tools:

* **get_stock_price** — Retrieves real-time stock prices and financial metrics using **yfinance**.
* **search_news** — Fetches the latest financial news using **DuckDuckGo Search**.

**schema.py** contains the Pydantic models used for validating the inputs and outputs of both tools, ensuring structured and type-safe data throughout the application.

The chatbot follows the **ReAct (Reason + Act)** paradigm. It reasons about the user's query, decides which tool(s) to invoke, observes the retrieved information, and generates a final natural-language response.

> **Note on LLM:** The problem statement requires an open-source Hugging Face model. Our implementation uses **Meta Llama 3.3 70B Instruct**, an open-source model, with inference served through the **Groq API**. This provides a reliable inference endpoint while preserving the use of the required open-source model.

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/STATIFY_2.0_Rangers-1.git
cd STATIFY_2.0_Rangers-1
```

> Replace the repository URL above with your actual GitHub repository link.

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open the `.env` file and add your API keys:

```env
HF_TOKEN=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
```

* **HF_TOKEN:** Obtain a free Hugging Face access token from https://huggingface.co/settings/tokens
* **GROQ_API_KEY:** Obtain a free Groq API key from https://console.groq.com

> **Important:** Never commit your `.env` file. It is already included in `.gitignore`.

---

## 4. Run the Chatbot

```bash
python3 Week1.py
```

---

# Example Queries

* What is the current stock price of Apple?
* Show me the latest news about Tesla.
* Give me a full analysis of Microsoft (MSFT).
* What is NVIDIA's P/E ratio and 52-week range?
* Summarize the latest market news for Amazon.

---

# Tech Stack

| Component            | Technology                                 |
| -------------------- | ------------------------------------------ |
| LLM                  | Meta Llama 3.3 70B Instruct (via Groq API) |
| Agent Framework      | LangChain ReAct                            |
| Stock Data           | yfinance                                   |
| News Search          | DuckDuckGo Search                          |
| Data Validation      | Pydantic                                   |
| Programming Language | Python                                     |
| User Interface       | Command-Line Interface (CLI)               |

---

# Project Structure

```text
STATIFY_2.0_Rangers/
│
├── Week1.py             # Main chatbot application
├── tool.py              # Financial tools
├── schema.py            # Pydantic schemas
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```
