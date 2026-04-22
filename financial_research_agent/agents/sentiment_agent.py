import os
import json
import google.generativeai as genai
from graph.state import ResearchState


def sentiment_agent(state: ResearchState) -> ResearchState:
    """
    Agent 2: Uses Claude to perform sentiment analysis on the news articles.
    Produces a structured sentiment breakdown written to state['sentiment_scores'].
    """
    articles = state.get("news_articles") or []
    ticker = state["ticker"]
    company_name = state["company_name"]

    print(f"[SentimentAgent] Analyzing sentiment for {len(articles)} articles...")

    if not articles:
        return {
            **state,
            "sentiment_scores": {
                "overall": "neutral",
                "score": 0.0,
                "breakdown": [],
                "summary": "No articles available for sentiment analysis.",
            },
            "current_step": "sentiment_done",
        }

    # Build a compact article list for the prompt
    articles_text = ""
    for i, a in enumerate(articles[:6], 1):
        articles_text += f"\n{i}. [{a['source']}] {a['title']}\n   {a.get('description', '')}\n"

    prompt = f"""You are a financial analyst AI. Analyze the sentiment of these news articles about {company_name} ({ticker}).

ARTICLES:
{articles_text}

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{{
  "overall": "bullish" | "bearish" | "neutral",
  "score": <float from -1.0 (very bearish) to 1.0 (very bullish)>,
  "confidence": "high" | "medium" | "low",
  "key_themes": ["theme1", "theme2", "theme3"],
  "risks": ["risk1", "risk2"],
  "catalysts": ["catalyst1", "catalyst2"],
  "breakdown": [
    {{"title": "...", "sentiment": "bullish|bearish|neutral", "score": 0.0}}
  ],
  "summary": "2-3 sentence narrative summary of the overall sentiment"
}}"""

    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Clean up any markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        sentiment_data = json.loads(raw)
        print(f"[SentimentAgent] Overall sentiment: {sentiment_data.get('overall')} (score: {sentiment_data.get('score')})")
        return {
            **state,
            "sentiment_scores": sentiment_data,
            "current_step": "sentiment_done",
        }

    except Exception as e:
        print(f"[SentimentAgent] Error: {e}")
        errors = state.get("errors") or []
        return {
            **state,
            "sentiment_scores": {
                "overall": "neutral",
                "score": 0.0,
                "breakdown": [],
                "summary": f"Sentiment analysis unavailable: {str(e)}",
            },
            "errors": errors + [f"SentimentAgent error: {str(e)}"],
            "current_step": "sentiment_done",
        }
