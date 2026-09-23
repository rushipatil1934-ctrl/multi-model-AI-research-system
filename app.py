import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind — Autonomous Research Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Design tokens & global styles ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0C1119;
    --surface: #131A26;
    --surface-raised: #171F2E;
    --border: rgba(255,255,255,0.08);
    --border-strong: rgba(255,255,255,0.14);
    --ink: #EDEFF3;
    --ink-dim: #9AA3B5;
    --ink-faint: #5B6478;
    --accent: #49C5B8;
    --accent-soft: rgba(73,197,184,0.12);
    --gold: #D9A94E;
    --gold-soft: rgba(217,169,78,0.12);
    --danger: #D9756A;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(circle at 12% 8%, rgba(73,197,184,0.06) 0%, transparent 42%),
        radial-gradient(circle at 88% 92%, rgba(217,169,78,0.05) 0%, transparent 45%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.2rem 3rem 4rem; max-width: 1180px; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.6rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.4rem;
}
.brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    color: var(--ink);
}
.brand-mark {
    color: var(--accent);
    font-size: 1rem;
}
.brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    color: var(--ink-faint);
    text-transform: uppercase;
    border: 1px solid var(--border-strong);
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
}

/* ── Hero ── */
.hero {
    padding: 1.4rem 0 2.8rem;
    max-width: 700px;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.1rem;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-optical-sizing: auto;
    font-size: clamp(2.4rem, 4.2vw, 3.4rem);
    font-weight: 500;
    line-height: 1.08;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0 0 1rem;
}
.hero h1 em {
    font-style: italic;
    color: var(--accent);
}
.hero-sub {
    font-size: 1rem;
    font-weight: 400;
    color: var(--ink-dim);
    line-height: 1.7;
    max-width: 560px;
}

/* ── Section labels ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink-faint);
    margin: 0 0 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Query console ── */
.console {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1.2rem;
}
.stTextInput > div > div > input {
    background: var(--surface-raised) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    color: var(--ink) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.92rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.15s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(73,197,184,0.14) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--ink-faint) !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #0C1119 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.7rem 1.4rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #5DD6C9 !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
}

/* ── Example chips ── */
.chip-row {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    flex-wrap: wrap;
    margin: 0.4rem 0 2.2rem;
}
.chip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.12em;
    color: var(--ink-faint);
    text-transform: uppercase;
}
.chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 0.32rem 0.75rem;
    font-size: 0.78rem;
    color: var(--ink-dim);
    font-family: 'Inter', sans-serif;
}

/* ── Pipeline rail (signature element) ── */
.rail {
    position: relative;
    padding-left: 2.4rem;
}
.rail-node {
    position: relative;
    padding-bottom: 2.1rem;
}
.rail-node:last-child { padding-bottom: 0; }
.rail-dot {
    position: absolute;
    left: -2.4rem;
    top: 0.25rem;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: var(--bg);
    border: 2px solid var(--ink-faint);
    box-sizing: border-box;
    z-index: 2;
}
.rail-line {
    position: absolute;
    left: calc(-2.4rem + 5.5px);
    top: 18px;
    bottom: -2.1rem;
    width: 2px;
    background: var(--border);
}
.rail-node:last-child .rail-line { display: none; }

.rail-node.is-running .rail-dot {
    border-color: var(--accent);
    background: var(--accent);
    box-shadow: 0 0 0 4px var(--accent-soft);
}
.rail-node.is-done .rail-dot {
    border-color: var(--gold);
    background: var(--gold);
}
.rail-node.is-done .rail-line {
    background: var(--gold-soft);
}

.rail-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--ink-faint);
    letter-spacing: 0.1em;
    margin-right: 0.5rem;
}
.rail-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--ink);
}
.rail-head {
    display: flex;
    align-items: baseline;
    gap: 0.3rem;
    margin-bottom: 0.25rem;
}
.rail-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
}
.rail-node.is-waiting .rail-status { color: var(--ink-faint); }
.rail-node.is-running .rail-status { color: var(--accent); }
.rail-node.is-done .rail-status { color: var(--gold); }
.rail-desc {
    font-size: 0.82rem;
    color: var(--ink-faint);
    line-height: 1.5;
    max-width: 340px;
}

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem 1.7rem;
}
.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--ink-faint);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--ink-dim);
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* ── Document panels (report / critique) ── */
.doc-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2.2rem 2.4rem;
    margin-top: 0.6rem;
}
.doc-panel.accent-gold { border-color: rgba(217,169,78,0.28); }
.doc-panel.accent-teal { border-color: rgba(73,197,184,0.28); }

.doc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}
.doc-label.teal { color: var(--accent); }
.doc-label.gold { color: var(--gold); }

.doc-panel .stMarkdown, .doc-panel p {
    font-family: 'Inter', sans-serif !important;
    color: var(--ink) !important;
    line-height: 1.75 !important;
}

/* ── Expander ── */
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.74rem !important;
    color: var(--ink-dim) !important;
    letter-spacing: 0.06em !important;
    cursor: pointer;
}
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    background: var(--surface) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--ink) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.55rem 1.1rem !important;
}
.stDownloadButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Divider ── */
.hairline {
    height: 1px;
    background: var(--border);
    margin: 2.6rem 0 2rem;
}

/* ── Footer ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--ink-faint);
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a pipeline rail node ──────────────────────────────────────
def rail_node(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": "PENDING",
        "running": "RUNNING",
        "done":    "COMPLETE",
    }
    st.markdown(f"""
    <div class="rail-node is-{state}">
        <div class="rail-line"></div>
        <div class="rail-dot"></div>
        <div class="rail-head">
            <span class="rail-num">{num}</span>
            <span class="rail-title">{title}</span>
            <span class="rail-status">{status_map.get(state, "")}</span>
        </div>
        <div class="rail-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="brand"><span class="brand-mark">◆</span> ResearchMind</div>
    <div class="brand-tag">Multi-Agent Pipeline</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Autonomous Research Intelligence</div>
    <h1>Four agents.<br>One <em>authoritative</em> report.</h1>
    <p class="hero-sub">
        Submit a topic and a coordinated agent pipeline handles the rest —
        sourcing current information, extracting depth from primary material,
        drafting a structured report, and independently reviewing it for quality.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="section-label">Query</div>', unsafe_allow_html=True)
    st.markdown('<div class="console">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("Run pipeline →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    chips_html = '<div class="chip-row"><span class="chip-label">Examples</span>'
    for ex in examples:
        chips_html += f'<span class="chip">{ex}</span>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-label">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def stage_state(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    st.markdown('<div class="rail">', unsafe_allow_html=True)
    rail_node("01", "Search Agent", stage_state("search"), "Gathers recent, reliable web information")
    rail_node("02", "Reader Agent", stage_state("reader"), "Scrapes and extracts deep source content")
    rail_node("03", "Writer Chain", stage_state("writer"), "Drafts the full structured research report")
    rail_node("04", "Critic Chain", stage_state("critic"), "Independently reviews and scores the report")
    st.markdown('</div>', unsafe_allow_html=True)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="hairline"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Output</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("Search results — raw agent output", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("Scraped content — raw agent output", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown('<div class="doc-panel accent-teal">', unsafe_allow_html=True)
        st.markdown('<div class="doc-label teal">Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            label="Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown('<div class="doc-panel accent-gold" style="margin-top:1.4rem;">', unsafe_allow_html=True)
        st.markdown('<div class="doc-label gold">Critic Review</div>', unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · LangChain multi-agent pipeline · Built on Streamlit
</div>
""", unsafe_allow_html=True)