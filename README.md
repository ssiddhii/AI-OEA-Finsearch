# 📊 FinResearch AI — Multi-Agent Financial Research System

> An agentic AI pipeline that autonomously researches any publicly traded company and synthesizes a professional investment brief — built with **LangGraph**, **Claude**, **yFinance**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-0.1+-purple)
![Claude](https://img.shields.io/badge/Anthropic-Claude-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)

---

## 🏗️ Architecture

```
User Input (Ticker)
        │
        ▼
┌──────────────────────────────────────────┐
│          Orchestrator (LangGraph)        │
│  StateGraph with shared ResearchState   │
└──────────────────────────────────────────┘
        │
   ┌────┼────────────┬──────────────┐
   ▼    ▼            ▼              ▼
News  Sentiment  Market Data    Report
Agent  Agent      Agent          Agent
  │      │            │              │
NewsAPI  Claude    yFinance       Claude
         (NLP)    (Financials)  (Synthesis)
        │
        ▼
  Investment Brief (Markdown)
```

### Agents

| Agent | Role | Tools |
|---|---|---|
| **News Agent** | Fetches recent headlines | NewsAPI |
| **Sentiment Agent** | NLP sentiment scoring + theme extraction | Gemini API |
| **Market Data Agent** | Stock price, fundamentals, technicals | yFinance |
| **Report Agent** | Synthesizes investment brief | Gemini API |

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/yourusername/finresearch-ai
cd finresearch-ai
pip install -r requirements.txt
```

### 2. Set up API keys

```bash
cp .env.example .env
# Edit .env and add your keys:
# GEMINI_API_KEY=sk-ant-...
# NEWS_API_KEY=...  (optional — mock news used if blank)
```

Get your keys:
- **Google AI Studio:** https://aistudio.google.com
- **NewsAPI (free):** https://newsapi.org

### 3. Run the app

```bash
streamlit run app.py
```

Or test via CLI:

```bash
python run.py AAPL
```

---

## 📦 Project Structure

```
finresearch-ai/
├── app.py                  # Streamlit UI
├── run.py                  # CLI runner
├── requirements.txt
├── .env.example
├── agents/
│   ├── news_agent.py       # Agent 1: news fetching
│   ├── sentiment_agent.py  # Agent 2: Claude NLP scoring
│   ├── market_agent.py     # Agent 3: yFinance data
│   └── report_agent.py     # Agent 4: Claude report synthesis
├── graph/
│   ├── state.py            # LangGraph ResearchState schema
│   └── pipeline.py         # StateGraph definition & entry point
└── tools/
    ├── news_tool.py        # NewsAPI wrapper
    └── market_tool.py      # yFinance wrapper
```

---

## 🎯 Features

- **Agentic pipeline** — 4 specialized agents orchestrated by LangGraph
- **Shared state** — all agents read/write a typed `ResearchState` dict
- **Sentiment analysis** — Claude scores each article and identifies themes, risks, catalysts
- **Financial metrics** — P/E, market cap, 52-week range, beta, margins, analyst targets
- **Interactive charts** — Plotly price history + sentiment gauge
- **Downloadable report** — full markdown investment brief
- **Graceful fallbacks** — mock news data if API key not set; error recovery at each agent

---

## 🔧 Extending the Project

- Add a **Macro Agent** that pulls Fed rate data from FRED API
- Add a **Competitor Agent** that compares the ticker against sector peers
- Add **LangGraph conditional edges** for error-recovery re-routing
- Store results in **SQLite** for historical brief comparison
- Deploy to **Streamlit Cloud** (free) for a public URL

---

## 📝 Tech Stack

| Component | Technology |
|---|---|
| Agent orchestration | LangGraph (StateGraph) |
| LLM | Google Gemini (Sonnet) |
| Stock data | yFinance |
| News data | NewsAPI |
| Frontend | Streamlit |
| Charts | Plotly |

---

## 👤 Author

Built as a portfolio project for financial AI / agentic systems.  
# Krutika Pingale UEC2023250
# Mahek Shah UEC2023258
# Sharwari Tijare UEC2023260
# Siddhi Chaudhari UEC2023263

---

*Disclaimer: This tool is for educpurposes only. It does not constitute financial advice.*
