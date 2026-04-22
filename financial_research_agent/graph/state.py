from typing import TypedDict, Optional, List


class ResearchState(TypedDict):
    """Shared state passed between all agents in the LangGraph pipeline."""

    # Input
    ticker: str
    company_name: str

    # Agent outputs
    news_articles: Optional[List[dict]]
    sentiment_scores: Optional[dict]
    market_data: Optional[dict]
    final_report: Optional[str]

    # Control
    errors: Optional[List[str]]
    current_step: Optional[str]
