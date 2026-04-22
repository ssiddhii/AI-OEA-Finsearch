from graph.state import ResearchState
from tools.market_tool import fetch_market_data


def market_data_agent(state: ResearchState) -> ResearchState:
    """
    Agent 3: Fetches current stock price, financial metrics, and price history.
    Writes structured market data to state['market_data'].
    """
    ticker = state["ticker"]
    print(f"[MarketDataAgent] Fetching market data for {ticker}...")

    try:
        data = fetch_market_data(ticker)

        # Update company name if yfinance returned a better one
        company_name = data.get("company_name") or state["company_name"]

        print(f"[MarketDataAgent] Current price: {data.get('current_price')} | Sector: {data.get('sector')}")
        return {
            **state,
            "company_name": company_name,
            "market_data": data,
            "current_step": "market_done",
        }
    except Exception as e:
        errors = state.get("errors") or []
        return {
            **state,
            "market_data": {"ticker": ticker, "error": str(e)},
            "errors": errors + [f"MarketDataAgent error: {str(e)}"],
            "current_step": "market_done",
        }
