from langgraph.graph import StateGraph, END

from graph.state import ResearchState
from agents.news_agent import news_agent
from agents.sentiment_agent import sentiment_agent
from agents.market_agent import market_data_agent
from agents.report_agent import report_agent


def build_graph() -> StateGraph:
    """
    Build and compile the LangGraph multi-agent pipeline.

    Flow:
        news_agent ──┐
                     ├──> report_agent ──> END
        market_agent─┘
             │
             └──> sentiment_agent ──> report_agent
    
    In practice we run sequentially for simplicity and reliability:
        news → sentiment → market → report → END
    """
    graph = StateGraph(ResearchState)

    # Register nodes
    graph.add_node("news_agent", news_agent)
    graph.add_node("sentiment_agent", sentiment_agent)
    graph.add_node("market_data_agent", market_data_agent)
    graph.add_node("report_agent", report_agent)

    # Define sequential edges
    graph.set_entry_point("news_agent")
    graph.add_edge("news_agent", "sentiment_agent")
    graph.add_edge("sentiment_agent", "market_data_agent")
    graph.add_edge("market_data_agent", "report_agent")
    graph.add_edge("report_agent", END)

    return graph.compile()


# Singleton — import this in app.py
research_pipeline = build_graph()


def run_research(ticker: str, company_name: str = "") -> ResearchState:
    """
    Entry point: run the full multi-agent pipeline for a given ticker.
    Returns the final ResearchState with all agent outputs.
    """
    if not company_name:
        company_name = ticker

    initial_state: ResearchState = {
        "ticker": ticker.upper(),
        "company_name": company_name,
        "news_articles": None,
        "sentiment_scores": None,
        "market_data": None,
        "final_report": None,
        "errors": [],
        "current_step": "start",
    }

    print(f"\n{'='*50}")
    print(f"  Starting research pipeline for {ticker.upper()}")
    print(f"{'='*50}\n")

    result = research_pipeline.invoke(initial_state)

    print(f"\n{'='*50}")
    print(f"  Pipeline complete for {ticker.upper()}")
    print(f"{'='*50}\n")

    return result
