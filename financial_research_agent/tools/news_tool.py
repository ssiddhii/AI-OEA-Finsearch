import os
import requests
from datetime import datetime, timedelta


def fetch_news(ticker: str, company_name: str) -> list[dict]:
    """
    Fetch recent news articles for a company using NewsAPI.
    Falls back to a mock response if API key is not set or quota exceeded.
    """
    api_key = os.getenv("NEWS_API_KEY", "")

    if api_key and api_key != "your_newsapi_key_here":
        try:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": f"{company_name} OR {ticker}",
                "from": from_date,
                "sortBy": "relevancy",
                "language": "en",
                "pageSize": 10,
                "apiKey": api_key,
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            if data.get("status") == "ok" and data.get("articles"):
                articles = []
                for a in data["articles"][:8]:
                    articles.append({
                        "title": a.get("title", ""),
                        "description": a.get("description", ""),
                        "source": a.get("source", {}).get("name", "Unknown"),
                        "published_at": a.get("publishedAt", ""),
                        "url": a.get("url", ""),
                    })
                return articles
        except Exception as e:
            print(f"[NewsAPI] Error: {e}. Falling back to mock data.")

    # Fallback: mock articles for demo purposes
    return [
        {
            "title": f"{company_name} reports strong quarterly earnings, beats analyst estimates",
            "description": f"{ticker} stock surges after the company announces revenue growth of 12% YoY, driven by strong performance in core business segments.",
            "source": "Financial Times (Mock)",
            "published_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": "#",
        },
        {
            "title": f"Analysts raise price target for {company_name} amid market optimism",
            "description": f"Multiple investment banks have upgraded their outlook on {ticker}, citing improved margins and positive macroeconomic tailwinds.",
            "source": "Bloomberg (Mock)",
            "published_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": "#",
        },
        {
            "title": f"{company_name} expands into new markets with strategic acquisition",
            "description": f"{ticker} announces acquisition deal aimed at diversifying its revenue base and entering high-growth emerging markets.",
            "source": "Reuters (Mock)",
            "published_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": "#",
        },
        {
            "title": f"Regulatory headwinds could pressure {company_name} in coming quarter",
            "description": f"Industry analysts warn of potential regulatory challenges for {ticker} as new compliance requirements take effect globally.",
            "source": "WSJ (Mock)",
            "published_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": "#",
        },
        {
            "title": f"{company_name} CEO outlines long-term growth strategy at investor day",
            "description": f"Leadership at {ticker} presented a bullish 5-year roadmap focused on technology investment, cost optimization, and shareholder returns.",
            "source": "CNBC (Mock)",
            "published_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "url": "#",
        },
    ]
