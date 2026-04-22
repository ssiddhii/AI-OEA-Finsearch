import yfinance as yf
from datetime import datetime


def fetch_market_data(ticker: str) -> dict:
    """
    Fetch current market data, financials, and key metrics for a ticker using yfinance.
    Returns a structured dict ready for agent consumption.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Price history (last 30 days)
        hist = stock.history(period="1mo")
        price_history = []
        if not hist.empty:
            for date, row in hist.iterrows():
                price_history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                })

        # Current price
        current_price = info.get("currentPrice") or info.get("regularMarketPrice") or (
            price_history[-1]["close"] if price_history else None
        )

        # Key metrics
        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "current_price": current_price,
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "50d_avg": info.get("fiftyDayAverage"),
            "200d_avg": info.get("twoHundredDayAverage"),
            "beta": info.get("beta"),
            "revenue": info.get("totalRevenue"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity"),
            "return_on_equity": info.get("returnOnEquity"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "analyst_recommendation": info.get("recommendationKey"),
            "target_price": info.get("targetMeanPrice"),
            "price_history": price_history[-20:],  # last 20 days for chart
            "business_summary": info.get("longBusinessSummary", "")[:500],
        }

    except Exception as e:
        # Return minimal fallback data if yfinance fails
        return {
            "ticker": ticker,
            "company_name": ticker,
            "current_price": None,
            "error": str(e),
            "price_history": [],
            "sector": "Unknown",
            "industry": "Unknown",
            "analyst_recommendation": "N/A",
        }
