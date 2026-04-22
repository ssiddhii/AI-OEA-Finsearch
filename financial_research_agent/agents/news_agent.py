from graph.state import ResearchState
from tools.news_tool import fetch_news


def news_agent(state: ResearchState) -> ResearchState:
    """
    Agent 1: Fetches recent news articles for the given ticker/company.
    Writes results to state['news_articles'].
    """
    ticker = state["ticker"]
    company_name = state["company_name"]

    print(f"[NewsAgent] Fetching news for {company_name} ({ticker})...")

    try:
        articles = fetch_news(ticker, company_name)
        print(f"[NewsAgent] Retrieved {len(articles)} articles.")
        return {
            **state,
            "news_articles": articles,
            "current_step": "news_done",
        }
    except Exception as e:
        errors = state.get("errors") or []
        return {
            **state,
            "news_articles": [],
            "errors": errors + [f"NewsAgent error: {str(e)}"],
            "current_step": "news_done",
        }
