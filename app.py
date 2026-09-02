import streamlit as st
import time
import json
from src.graph import research_app
from src.state import ResearchState

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Enterprise Multi-Agent System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1280px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 0.8rem;
}
.hero h1 span {
    color: #ff8c32;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Badges ── */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.badge-item {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 0.25rem 0.6rem;
    border-radius: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #c0b8b0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 1.8rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f0ebe0 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.5);
    background: rgba(255,140,50,0.05);
}
.step-card.done {
    border-color: rgba(80,200,120,0.35);
    background: rgba(80,200,120,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: rgba(255,255,255,0.05);
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    color: #ff8c32;
    opacity: 0.8;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
}
.status-waiting  { color: #555; }
.status-running  { color: #ff8c32; }
.status-done     { color: #50c878; }

/* ── HUD / Telemetry card ── */
.hud-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.hud-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.hud-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #a09890;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.hud-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #ff8c32;
}

/* ── Panels ── */
.report-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,140,50,0.25);
    border-radius: 16px;
    padding: 2.2rem;
    margin-bottom: 1.5rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(80,200,120,0.25);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.panel-label.orange { color: #ff8c32; }
.panel-label.green  { color: #50c878; }
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ─────────────────────────────────────────────
if "state_data" not in st.session_state:
    st.session_state.state_data = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""


def step_card(num, title, state, desc=""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("EXECUTING…", "status-running"),
        "done":    ("COMPLETED", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.78rem;color:#807870;margin-top:0.2rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Hero Section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Enterprise Multi-Agent Architecture</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Production-grade autonomous research orchestrated by <b>LangGraph</b>.
        Features query decomposition, deep web scraping, publication-grade synthesis,
        and an automated <b>reflection loop</b> with structured Pydantic audit.
    </p>
    <div class="badge-row">
        <span class="badge-item">⚡ LangGraph StateGraph</span>
        <span class="badge-item">🧠 Mistral-Small</span>
        <span class="badge-item">🔎 Tavily Search API</span>
        <span class="badge-item">🛡️ Pydantic Reflection Loop</span>
        <span class="badge-item">🐍 Python 3.12</span>
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: Input vs Pipeline Status ────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.4, 4.2])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic_val = st.text_input(
        "RESEARCH TOPIC OR HYPOTHESIS",
        value=st.session_state.topic_input,
        placeholder="e.g. Agentic AI Workflows and Self-Correcting LLM Architecture 2025",
        key="topic_field",
    )

    run_btn = st.button("🚀  Launch Multi-Agent Graph", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.75rem;color:#a09890;margin-bottom:0.8rem;letter-spacing:0.1em;">ORCHESTRATION PIPELINE</div>', unsafe_allow_html=True)

    sd = st.session_state.state_data
    is_running = st.session_state.running

    def get_step_state(node_key):
        if node_key in sd:
            return "done"
        if is_running:
            # Active step logic
            if node_key == "planner" and "sub_queries" not in sd:
                return "running"
            if node_key == "researcher" and "sub_queries" in sd and "search_results" not in sd:
                return "running"
            if node_key == "curator" and "search_results" in sd and "scraped_sources" not in sd:
                return "running"
            if node_key == "writer" and "scraped_sources" in sd and "draft_report" not in sd:
                return "running"
            if node_key == "critic" and "draft_report" in sd and "critic_review" not in sd:
                return "running"
        return "waiting"

    step_card("01", "Planner Agent",
              "done" if "sub_queries" in sd else ("running" if is_running and "sub_queries" not in sd else "waiting"),
              "Decomposes topic into targeted search angles")

    step_card("02", "Researcher Agent",
              "done" if "search_results" in sd else ("running" if is_running and "sub_queries" in sd and "search_results" not in sd else "waiting"),
              "Executes multi-query Tavily web searches")

    step_card("03", "Curator Agent",
              "done" if "scraped_sources" in sd else ("running" if is_running and "search_results" in sd and "scraped_sources" not in sd else "waiting"),
              "Deep content extraction & HTML cleaning")

    step_card("04", "Writer Agent",
              "done" if "draft_report" in sd else ("running" if is_running and "scraped_sources" in sd and "draft_report" not in sd else "waiting"),
              "Synthesizes formal report with inline citations")

    step_card("05", "Critic Agent (Reflection Loop)",
              "done" if "critic_review" in sd else ("running" if is_running and "draft_report" in sd and "critic_review" not in sd else "waiting"),
              "Rigorous Pydantic quality audit & revision gating")


# ── Execution Trigger ────────────────────────────────────────────────────────
if run_btn:
    chosen_topic = topic_val.strip() if topic_val.strip() else st.session_state.topic_input.strip()
    if not chosen_topic:
        st.warning("Please provide a research topic or click a benchmark preset.")
    else:
        st.session_state.topic_input = chosen_topic
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.state_data = {}
        st.rerun()


# ── Graph Streaming Execution ────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    current_topic = st.session_state.topic_input

    initial_graph_state: ResearchState = {
        "topic": current_topic,
        "sub_queries": [],
        "search_results": [],
        "scraped_sources": [],
        "draft_report": "",
        "critic_review": None,
        "revision_count": 0,
        "revision_notes": [],
        "current_node": "start",
        "timeline": [],
    }

    accumulated_state = dict(initial_graph_state)
    status_placeholder = st.empty()

    with status_placeholder.container():
        with st.spinner("🤖 Autonomous multi-agent graph running..."):
            for event in research_app.stream(initial_graph_state, stream_mode="updates"):
                for node_name, node_update in event.items():
                    accumulated_state.update(node_update)
                    st.session_state.state_data = dict(accumulated_state)

    status_placeholder.empty()
    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results & Telemetry Display ──────────────────────────────────────────────
final_data = st.session_state.state_data

if final_data.get("draft_report"):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:700;color:#f0ebe0;margin-bottom:1.2rem;">Execution Telemetry & Findings</div>', unsafe_allow_html=True)

    # Telemetry HUD
    total_duration = sum(e.get("duration_seconds", 0) for e in final_data.get("timeline", []))
    sources_count = len(final_data.get("search_results", []))
    scraped_count = len(final_data.get("scraped_sources", []))
    review = final_data.get("critic_review") or {}
    score = review.get("score", "N/A")
    revisions = final_data.get("revision_count", 1)

    st.markdown(f"""
    <div class="hud-grid">
        <div class="hud-card">
            <div class="hud-label">Total Execution Time</div>
            <div class="hud-val">{round(total_duration, 1)}s</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Sources Gathered</div>
            <div class="hud-val">{sources_count} <span style="font-size:0.8rem;color:#807870;">({scraped_count} Scraped)</span></div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Revision Cycles</div>
            <div class="hud-val">{revisions}</div>
        </div>
        <div class="hud-card">
            <div class="hud-label">Critic Quality Score</div>
            <div class="hud-val" style="color: {'#50c878' if str(score) >= '8' else '#ff8c32'}">{score}/10</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_report, tab_critic, tab_inspector = st.tabs(["📝 Executive Research Report", "🧐 Structured Critic Audit", "🔬 Multi-Agent Inspector"])

    with tab_report:
        st.markdown('<div class="report-panel"><div class="panel-label orange">Verified Research Report</div>', unsafe_allow_html=True)
        st.markdown(final_data["draft_report"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Download buttons
        d_col1, d_col2 = st.columns([2, 8])
        with d_col1:
            st.download_button(
                label="⬇ Download Report (.md)",
                data=final_data["draft_report"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with d_col2:
            st.download_button(
                label="⬇ Export Full Session (.json)",
                data=json.dumps(final_data, indent=2, default=str),
                file_name=f"agent_session_{int(time.time())}.json",
                mime="application/json",
            )

    with tab_critic:
        if review:
            st.markdown('<div class="feedback-panel">', unsafe_allow_html=True)
            st.markdown(f'<div class="panel-label green">Audit Outcome: {"APPROVED (PUBLICATION READY)" if review.get("passed") else "REVISION REQUIRED"}</div>', unsafe_allow_html=True)

            st.write(f"**Executive Verdict:** {review.get('verdict')}")

            # Criterion scores
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Factual Accuracy", f"{review.get('factual_accuracy', 'N/A')}/10")
            c2.metric("Depth & Coverage", f"{review.get('depth_and_coverage', 'N/A')}/10")
            c3.metric("Structure & Clarity", f"{review.get('structure_and_clarity', 'N/A')}/10")
            c4.metric("Citation Quality", f"{review.get('citation_quality', 'N/A')}/10")

            st.markdown("---")
            k_col1, k_col2 = st.columns(2)
            with k_col1:
                st.markdown("##### 🌟 Key Strengths Identified")
                for s in review.get("strengths", []):
                    st.markdown(f"- {s}")
            with k_col2:
                st.markdown("##### ⚠️ Improvement Recommendations")
                for r in review.get("actionable_recommendations", []):
                    st.markdown(f"- {r}")

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No critic review data recorded.")

    with tab_inspector:
        st.markdown("#### 1. Strategic Query Plan (Planner Agent)")
        for i, q in enumerate(final_data.get("sub_queries", []), 1):
            st.markdown(f"**{i}.** `{q}`")

        st.markdown("#### 2. Search Results (Researcher Agent)")
        with st.expander(f"View {len(final_data.get('search_results', []))} Search Snippets", expanded=False):
            for item in final_data.get("search_results", []):
                st.markdown(f"- **[{item.get('title')}]({item.get('url')})**")
                st.caption(item.get("content", ""))

        st.markdown("#### 3. Deep Web Content (Curator Agent)")
        with st.expander(f"View {len(final_data.get('scraped_sources', []))} Full Body Text Scrapes", expanded=False):
            for sc in final_data.get("scraped_sources", []):
                st.markdown(f"**Source:** [{sc.get('title')}]({sc.get('url')})")
                st.text(sc.get("content", "")[:1200] + "...")

        st.markdown("#### 4. Execution Graph Timeline")
        st.table([
            {
                "Stage": ev.get("stage"),
                "Agent": ev.get("node"),
                "Duration": f"{ev.get('duration_seconds')}s",
                "Details": ev.get("details", "")[:80],
            }
            for ev in final_data.get("timeline", [])
        ])

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;font-family:'DM Mono',monospace;font-size:0.7rem;color:#605850;">
    ResearchMind · LangGraph StateGraph Multi-Agent System · Production-Grade Architecture
</div>
""", unsafe_allow_html=True)