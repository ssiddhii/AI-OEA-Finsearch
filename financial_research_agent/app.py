import os
import sys
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinResearch AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3a5f, #2e86ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #2e86ab;
        margin-bottom: 0.8rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.3rem;
    }
    .bullish { color: #27ae60; font-weight: 700; font-size: 1.1rem; }
    .bearish { color: #e74c3c; font-weight: 700; font-size: 1.1rem; }
    .neutral { color: #f39c12; font-weight: 700; font-size: 1.1rem; }
    .stProgress > div > div { background-color: #2e86ab; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    gemini_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get yours at aistudio.google.com",
    )
    news_key = st.text_input(
        "NewsAPI Key (optional)",
        value=os.getenv("NEWS_API_KEY", ""),
        type="password",
        help="Free at newsapi.org — if blank, mock news is used",
    )

    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    if news_key:
        os.environ["NEWS_API_KEY"] = news_key

    st.markdown("---")
    st.markdown("### 🤖 Agent Pipeline")
    st.markdown("""
    1. **News Agent** — fetches headlines  
    2. **Sentiment Agent** — Gemini NLP scoring  
    3. **Market Agent** — yFinance data  
    4. **Report Agent** — Gemini synthesis  
    """)

    st.markdown("---")
    st.markdown("### 📌 Example Tickers")
    example_cols = st.columns(2)
    examples = ["AAPL", "MSFT", "GOOGL", "JPM", "TSLA", "NVDA"]
    for i, ex in enumerate(examples):
        if example_cols[i % 2].button(ex, use_container_width=True):
            st.session_state["ticker_input"] = ex

    st.markdown("---")
    st.caption("Built with LangGraph + Claude + yFinance")


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📊 FinResearch AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent Financial Research System · Powered by LangGraph & Claude</p>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    ticker = st.text_input(
        "Enter stock ticker",
        value=st.session_state.get("ticker_input", ""),
        placeholder="e.g. AAPL, TSLA, JPM",
        label_visibility="collapsed",
    ).upper().strip()
with col2:
    run_btn = st.button("🔍 Run Research", type="primary", use_container_width=True)
with col3:
    if st.button("🗑️ Clear", use_container_width=True):
        for key in ["result", "ticker_input"]:
            st.session_state.pop(key, None)
        st.rerun()

# ── Validation ────────────────────────────────────────────────────────────────
if run_btn:
    if not ticker:
        st.warning("Please enter a ticker symbol.")
    elif not os.getenv("GEMINI_API_KEY"):
        st.error("Please enter your Anthropic API key in the sidebar.")
    else:
        st.session_state["ticker_input"] = ticker

        # Run pipeline with progress
        progress_bar = st.progress(0)
        status = st.empty()

        steps = [
            ("🗞️ News Agent fetching headlines...", 20),
            ("🧠 Sentiment Agent analyzing tone...", 45),
            ("📈 Market Agent pulling price data...", 65),
            ("✍️ Report Agent synthesizing brief...", 90),
        ]

        with st.spinner("Running multi-agent pipeline..."):
            # Import here to avoid module load errors before keys are set
            from graph.pipeline import run_research

            # Simulate step updates
            import threading
            import time

            result_container = {}

            def run_pipeline():
                result_container["result"] = run_research(ticker)

            thread = threading.Thread(target=run_pipeline)
            thread.start()

            step_idx = 0
            while thread.is_alive():
                if step_idx < len(steps):
                    label, pct = steps[step_idx]
                    status.markdown(f"**{label}**")
                    progress_bar.progress(pct)
                    step_idx += 1
                time.sleep(3)
                if not thread.is_alive():
                    break

            thread.join()
            progress_bar.progress(100)
            status.markdown("**✅ Research complete!**")

        st.session_state["result"] = result_container.get("result")
        time.sleep(0.5)
        progress_bar.empty()
        status.empty()


# ── Results ───────────────────────────────────────────────────────────────────
if "result" in st.session_state and st.session_state["result"]:
    result = st.session_state["result"]
    market = result.get("market_data") or {}
    sentiment = result.get("sentiment_scores") or {}
    articles = result.get("news_articles") or []
    report = result.get("final_report") or ""

    st.markdown("---")

    # ── Top metrics row
    company = result.get("company_name", ticker)
    st.subheader(f"📋 {company} ({result.get('ticker', '')})")

    m1, m2, m3, m4, m5 = st.columns(5)

    price = market.get("current_price")
    m1.metric("Current Price", f"${price:,.2f}" if price else "N/A")

    pe = market.get("pe_ratio")
    m2.metric("P/E Ratio", f"{pe:.1f}x" if pe else "N/A")

    cap = market.get("market_cap")
    if cap:
        cap_str = f"${cap/1e12:.2f}T" if cap > 1e12 else f"${cap/1e9:.1f}B"
    else:
        cap_str = "N/A"
    m3.metric("Market Cap", cap_str)

    rec = market.get("analyst_recommendation", "N/A")
    m4.metric("Analyst Rec.", rec.upper() if rec else "N/A")

    s_score = sentiment.get("score", 0)
    m5.metric("Sentiment Score", f"{s_score:+.2f}", delta=None)

    st.markdown("---")

    # ── Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Data", "🧠 Sentiment", "🗞️ News", "📄 Full Report"])

    # ── Tab 1: Market Data
    with tab1:
        left, right = st.columns([3, 2])

        with left:
            st.markdown("#### Price History (Last 30 Days)")
            price_hist = market.get("price_history", [])
            if price_hist:
                df = pd.DataFrame(price_hist)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df["date"], y=df["close"],
                    mode="lines+markers",
                    line=dict(color="#2e86ab", width=2),
                    marker=dict(size=4),
                    fill="tozeroy",
                    fillcolor="rgba(46,134,171,0.1)",
                    name="Close Price",
                ))
                fig.update_layout(
                    height=300, margin=dict(l=0, r=0, t=10, b=0),
                    xaxis_title="", yaxis_title="Price (USD)",
                    hovermode="x unified", showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Price history not available.")

        with right:
            st.markdown("#### Key Metrics")
            metrics = {
                "52W High": f"${market.get('52w_high'):,.2f}" if market.get('52w_high') else "N/A",
                "52W Low": f"${market.get('52w_low'):,.2f}" if market.get('52w_low') else "N/A",
                "50D Avg": f"${market.get('50d_avg'):,.2f}" if market.get('50d_avg') else "N/A",
                "Beta": f"{market.get('beta'):.2f}" if market.get('beta') else "N/A",
                "EPS": f"${market.get('eps'):.2f}" if market.get('eps') else "N/A",
                "Dividend Yield": f"{market.get('dividend_yield')*100:.2f}%" if market.get('dividend_yield') else "N/A",
                "Profit Margin": f"{market.get('profit_margin')*100:.1f}%" if market.get('profit_margin') else "N/A",
                "ROE": f"{market.get('return_on_equity')*100:.1f}%" if market.get('return_on_equity') else "N/A",
                "D/E Ratio": f"{market.get('debt_to_equity'):.2f}" if market.get('debt_to_equity') else "N/A",
                "Price Target": f"${market.get('target_price'):,.2f}" if market.get('target_price') else "N/A",
            }
            for k, v in metrics.items():
                c1, c2 = st.columns([1, 1])
                c1.caption(k)
                c2.markdown(f"**{v}**")

    # ── Tab 2: Sentiment
    with tab2:
        s1, s2 = st.columns([1, 2])

        with s1:
            st.markdown("#### Overall Sentiment")
            overall = sentiment.get("overall", "neutral")
            score = sentiment.get("score", 0)
            css_class = overall if overall in ["bullish", "bearish"] else "neutral"
            emoji = "🟢" if overall == "bullish" else ("🔴" if overall == "bearish" else "🟡")
            st.markdown(f'<p class="{css_class}">{emoji} {overall.upper()}</p>', unsafe_allow_html=True)
            st.markdown(f"**Score:** {score:+.2f}")
            st.markdown(f"**Confidence:** {sentiment.get('confidence', 'N/A').title()}")

            # Gauge chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [-1, 1]},
                    "bar": {"color": "#2e86ab"},
                    "steps": [
                        {"range": [-1, -0.3], "color": "#fadbd8"},
                        {"range": [-0.3, 0.3], "color": "#fef9e7"},
                        {"range": [0.3, 1], "color": "#d5f5e3"},
                    ],
                    "threshold": {"line": {"color": "black", "width": 3}, "thickness": 0.75, "value": score},
                },
            ))
            fig_gauge.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with s2:
            st.markdown("#### Themes & Signals")
            themes = sentiment.get("key_themes", [])
            if themes:
                st.markdown("**Key Themes**")
                for t in themes:
                    st.markdown(f"• {t}")

            risks = sentiment.get("risks", [])
            cats = sentiment.get("catalysts", [])

            r1, r2 = st.columns(2)
            with r1:
                st.markdown("**⚠️ Risks**")
                for r in risks:
                    st.markdown(f"• {r}")
            with r2:
                st.markdown("**🚀 Catalysts**")
                for c in cats:
                    st.markdown(f"• {c}")

            st.markdown(f"\n**Narrative:** {sentiment.get('summary', '')}")

            # Per-article breakdown
            breakdown = sentiment.get("breakdown", [])
            if breakdown:
                st.markdown("#### Article-Level Sentiment")
                for item in breakdown:
                    s = item.get("sentiment", "neutral")
                    color = "🟢" if s == "bullish" else ("🔴" if s == "bearish" else "🟡")
                    score_val = item.get("score", 0)
                    st.markdown(f"{color} **{item.get('title', '')[:80]}...** — `{s}` ({score_val:+.2f})")

    # ── Tab 3: News
    with tab3:
        st.markdown(f"#### Latest News ({len(articles)} articles)")
        for i, article in enumerate(articles):
            with st.expander(f"📰 {article.get('title', 'Article')[:90]}"):
                st.markdown(f"**Source:** {article.get('source', 'Unknown')} | **Published:** {article.get('published_at', '')[:10]}")
                st.markdown(article.get("description", "No description available."))
                if article.get("url") and article["url"] != "#":
                    st.markdown(f"[Read full article →]({article['url']})")

    # ── Tab 4: Full Report
    with tab4:
        st.markdown("#### 📄 AI-Generated Investment Brief")

        dl_col, _ = st.columns([1, 3])
        dl_col.download_button(
            label="⬇️ Download Report (MD)",
            data=report,
            file_name=f"{result.get('ticker', 'report')}_research_brief.md",
            mime="text/markdown",
        )
        st.markdown("---")
        st.markdown(report)

    # ── Errors
    errors = result.get("errors") or []
    if errors:
        with st.expander("⚠️ Pipeline warnings"):
            for e in errors:
                st.warning(e)

else:
    # Landing state
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0; color: #999;">
        <h2>🔍 Enter a ticker symbol above to begin</h2>
        <p>The AI pipeline will fetch news, analyze sentiment, pull market data,<br>
        and synthesize a professional investment brief — all automatically.</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature cards
    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, desc in [
        (c1, "🗞️", "News Agent", "Fetches recent headlines from NewsAPI"),
        (c2, "🧠", "Sentiment Agent", "Gemini NLP scores tone & themes"),
        (c3, "📈", "Market Agent", "yFinance prices & fundamentals"),
        (c4, "✍️", "Report Agent", "Gemini synthesizes investment brief"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <h3>{icon} {title}</h3>
            <p style="color:#666;font-size:0.9rem">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
