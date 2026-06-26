"""
schema.py — Pydantic models for tool input/output validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ── Tool Inputs ────────────────────────────────────────────────────────────────

class StockPriceInput(BaseModel):
    """Input schema for the real-time stock price tool."""
    ticker: str = Field(
        ...,
        description="The stock ticker symbol (e.g. 'AAPL', 'TSLA', 'MSFT').",
    )


class NewsSearchInput(BaseModel):
    """Input schema for the DuckDuckGo news search tool."""
    query: str = Field(
        ...,
        description="Search query string — typically the company name plus 'stock news'.",
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of news results to return.",
    )


# ── Tool Outputs ───────────────────────────────────────────────────────────────

class StockPriceOutput(BaseModel):
    """Structured response returned by the stock price tool."""
    ticker: str
    company_name: Optional[str] = None
    current_price: Optional[float] = None
    currency: Optional[str] = "USD"
    previous_close: Optional[float] = None
    day_open: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    error: Optional[str] = None

    def to_summary(self) -> str:
        """Return a human-readable summary for the LLM context."""
        if self.error:
            return f"[Stock Error] {self.ticker}: {self.error}"
        lines = [
            f"📈 {self.company_name or self.ticker} ({self.ticker})",
            f"   Current Price : {self.currency} {self.current_price:.2f}" if self.current_price else "",
            f"   Previous Close: {self.currency} {self.previous_close:.2f}" if self.previous_close else "",
            f"   Open / High / Low: {self.day_open} / {self.day_high} / {self.day_low}",
            f"   Volume        : {self.volume:,}" if self.volume else "",
            f"   52-Week Range : {self.fifty_two_week_low} – {self.fifty_two_week_high}",
            f"   Market Cap    : {self.market_cap:,.0f}" if self.market_cap else "",
            f"   P/E Ratio     : {self.pe_ratio}" if self.pe_ratio else "",
        ]
        return "\n".join(l for l in lines if l)


class NewsArticle(BaseModel):
    """A single news article."""
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None
    source: Optional[str] = None
    published: Optional[str] = None


class NewsSearchOutput(BaseModel):
    """Structured response returned by the news search tool."""
    query: str
    articles: List[NewsArticle] = []
    error: Optional[str] = None

    def to_summary(self) -> str:
        """Return a human-readable summary for the LLM context."""
        if self.error:
            return f"[News Error] {self.error}"
        if not self.articles:
            return f"No news found for: {self.query}"
        lines = [f"📰 Latest news for '{self.query}':"]
        for i, a in enumerate(self.articles, 1):
            lines.append(f"\n  {i}. {a.title}")
            if a.source:
                lines.append(f"     Source : {a.source}")
            if a.published:
                lines.append(f"     Date   : {a.published}")
            if a.snippet:
                lines.append(f"     Snippet: {a.snippet[:200]}...")
            if a.url:
                lines.append(f"     URL    : {a.url}")
        return "\n".join(lines)


# ── Agent Response ─────────────────────────────────────────────────────────────

class AgentResponse(BaseModel):
    """Top-level structured response from the financial analyst agent."""
    user_query: str
    answer: str
    stock_data: Optional[StockPriceOutput] = None
    news_data: Optional[NewsSearchOutput] = None
    sources_used: List[str] = []
