"""
tool.py — LangChain-compatible tools for the financial analyst chatbot.

Tools:
  1. get_stock_price  — fetches live stock data via yfinance
  2. search_news      — retrieves latest news via DuckDuckGo
"""

import json
import yfinance as yf
from duckduckgo_search import DDGS
from langchain.tools import tool

from schema import (
    StockPriceInput,
    StockPriceOutput,
    NewsSearchInput,
    NewsSearchOutput,
    NewsArticle,
)


# ── Tool 1: Real-Time Stock Price ──────────────────────────────────────────────

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker: str) -> str:
    """
    Fetch real-time stock price and key financial metrics for a given ticker symbol.
    Use this tool whenever the user asks about a stock's current price, market cap,
    P/E ratio, 52-week range, or general price information.

    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'TSLA', 'GOOGL').

    Returns:
        A formatted string with live stock data.
    """
    ticker = ticker.strip().upper()
    try:
        t = yf.Ticker(ticker)
        info = t.info

        # yfinance may return an empty dict for invalid tickers
        if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
            output = StockPriceOutput(
                ticker=ticker,
                error=f"No data found for ticker '{ticker}'. Please check the symbol.",
            )
            return output.to_summary()

        output = StockPriceOutput(
            ticker=ticker,
            company_name=info.get("longName") or info.get("shortName"),
            current_price=info.get("currentPrice") or info.get("regularMarketPrice"),
            currency=info.get("currency", "USD"),
            previous_close=info.get("previousClose") or info.get("regularMarketPreviousClose"),
            day_open=info.get("open") or info.get("regularMarketOpen"),
            day_high=info.get("dayHigh") or info.get("regularMarketDayHigh"),
            day_low=info.get("dayLow") or info.get("regularMarketDayLow"),
            volume=info.get("volume") or info.get("regularMarketVolume"),
            market_cap=info.get("marketCap"),
            pe_ratio=info.get("trailingPE"),
            fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
            fifty_two_week_low=info.get("fiftyTwoWeekLow"),
        )
        return output.to_summary()

    except Exception as e:
        output = StockPriceOutput(
            ticker=ticker,
            error=str(e),
        )
        return output.to_summary()


# ── Tool 2: Live News Search ───────────────────────────────────────────────────

@tool("search_news", args_schema=NewsSearchInput)
def search_news(query: str, max_results: int = 5) -> str:
    """
    Search the web for the latest financial news, market updates, and analyst
    sentiment for a given company or topic using DuckDuckGo.
    Use this tool whenever the user asks about recent news, headlines, analyst
    opinions, or market sentiment for a stock or company.

    Args:
        query:       Search query (e.g. 'Apple AAPL stock news 2025').
        max_results: Number of articles to return (default 5, max 10).

    Returns:
        A formatted string with recent news articles and snippets.
    """
    try:
        articles = []
        with DDGS() as ddgs:
            results = ddgs.news(
                keywords=query,
                max_results=max_results,
            )
            for r in results:
                articles.append(
                    NewsArticle(
                        title=r.get("title", "No title"),
                        url=r.get("url"),
                        snippet=r.get("body"),
                        source=r.get("source"),
                        published=r.get("date"),
                    )
                )

        output = NewsSearchOutput(query=query, articles=articles)
        return output.to_summary()

    except Exception as e:
        output = NewsSearchOutput(query=query, error=str(e))
        return output.to_summary()


# ── Exported tool list ─────────────────────────────────────────────────────────

TOOLS = [get_stock_price, search_news]
