"""Reusable presentation helpers for the Streamlit dashboard."""

from html import escape

import streamlit as st


def load_css() -> None:
    """Apply the product dashboard's restrained dark theme."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0');
        :root {
            --bg: #0B0F1A;
            --panel: #121929;
            --border: rgba(255,255,255,.09);
            --muted: #9AA8C0;
            --text: #E8EEF9;
            --indigo: #6366F1;
            --green: #10B981;
            --red: #EF4444;
        }
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        .stApp { color: var(--text); background: var(--bg); }
        [data-testid="stHeader"] { background: transparent; }
        #MainMenu, footer { visibility: hidden; }
        .block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 4rem; }
        h1, h2, h3, [data-testid="stMetricLabel"] { letter-spacing: -.025em; }
        p, label, [data-testid="stCaptionContainer"] { color: #B5C0D4; }
        .material-symbols-rounded { font-family: 'Material Symbols Rounded'; font-weight: normal; font-style: normal; }
        .hero { padding: 1.5rem 1.65rem; margin-bottom: 1rem; border: 1px solid var(--border);
            border-radius: 14px; background: var(--panel); }
        .hero-kicker { color: #AAB7CC; font-size: .72rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }
        .hero-title { margin: .4rem 0 .35rem; color: #F1F5FC; font-size: clamp(1.8rem,3vw,2.4rem); line-height: 1.15; }
        .hero-copy { margin: 0; color: #AAB7CC; font-size: .95rem; }
        .metric-card { box-sizing: border-box; display: flex; flex-direction: column; height: 144px; min-height: 144px;
            padding: 1rem 1.05rem; margin-bottom: 1.25rem; border: 1px solid var(--border); border-radius: 14px; background: var(--panel); }
        .metric-top { display:flex; align-items:center; justify-content:space-between; color:var(--muted); font-size:.75rem; font-weight:600; }
        .metric-icon { color:#8B93FF; font-size:1.2rem; }
        .metric-value { display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:2; overflow:hidden;
            margin-top:.55rem; color:#F1F5FC; font:600 1.05rem 'Inter',sans-serif; overflow-wrap:anywhere; }
        .metric-detail { display:-webkit-box; -webkit-box-orient:vertical; -webkit-line-clamp:1; overflow:hidden;
            color:var(--muted); font-size:.72rem; margin-top:auto; padding-top:.35rem; }
        .section-eyebrow { margin:1.25rem 0 .5rem; color:#8F9DB5; font-size:.68rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase; }
        .glass-card { padding:1rem 1.1rem; border:1px solid var(--border); border-radius:14px; background:var(--panel); }
        .preset-copy { min-height:2.1rem; margin:.1rem .1rem .5rem; color:#95A3BA; font-size:.75rem; line-height:1.45; }
        div.stButton > button { min-height:3rem; border-radius:9px; font-weight:600; line-height:1.3; white-space:normal; }
        div.stButton > button[kind="primary"] { color:white; border:1px solid #4F46E5; background:#4F46E5; margin-top:1rem !important; margin-bottom:0.75rem !important; }
        div.stButton > button[kind="primary"]:hover { border-color:#6366F1; background:#5558E8; }
        div.stButton > button[kind="secondary"] { color:#DCE5F4; border:1px solid rgba(148,163,184,.3); background:rgba(255,255,255,.025); }
        div.stButton > button[kind="secondary"]:hover { color:white; border-color:#818CF8; background:rgba(99,102,241,.1); }
        input, textarea, [data-baseweb="select"] > div { background-color:rgba(10,15,27,.72) !important; }
        input:focus, textarea:focus { border-color:#818CF8 !important; box-shadow:0 0 0 1px #6366F1,0 0 18px rgba(99,102,241,.18) !important; }
        [data-testid="stExpander"], [data-testid="stTabs"] [role="tablist"] { border-color:var(--border); }
        [data-testid="stExpander"] { border-radius:14px; background:rgba(17,24,39,.52); }
        [data-testid="stFileUploader"] { padding:.7rem; border:1px dashed rgba(129,140,248,.42);
            border-radius:14px; background:rgba(99,102,241,.045); }
        [data-testid="stDownloadButton"] { width:100%; }
        [data-testid="stDownloadButton"] button { width:100%; min-height:3.35rem; white-space:normal;
            line-height:1.3; justify-content:center; text-align:center; }
        [data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid var(--border); border-radius:12px; overflow:hidden; }
        [data-testid="stMetric"] { padding:.85rem 1rem; border:1px solid var(--border); border-radius:14px; background:var(--panel); }
        [data-testid="stMetricValue"] { color:#EDF3FF; }
        [data-testid="stAlert"] { border-radius:14px; }
        [data-testid="stSidebar"] { background:#101728; border-right:1px solid var(--border); }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] hr { border-color:rgba(255,255,255,.1); }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { letter-spacing:-.02em; }
        .sidebar-brand { display:flex; align-items:center; gap:.7rem; padding:.8rem .7rem 1.1rem; margin-bottom:.4rem;
            border-bottom:1px solid var(--border); color:#F2F5FC; font:600 1rem 'Inter',sans-serif; }
        .brand-mark { display:grid; place-items:center; width:34px; height:34px; border-radius:9px; color:white; background:#4F46E5; }
        .terminal { padding:1rem; border:1px solid var(--border); border-radius:12px; background:#080D16; color:#C4D0E3;
            font: .78rem/1.7 'Cascadia Code','Consolas',monospace; white-space:pre-wrap; overflow-wrap:anywhere; }
        .stepper { display:grid; grid-template-columns:repeat(7,minmax(90px,1fr)); gap:.5rem; padding:.6rem 0 1rem; overflow-x:auto; }
        .step { position:relative; min-width:90px; padding:.7rem .45rem; text-align:center; border:1px solid var(--border); border-radius:10px; background:rgba(255,255,255,.025); }
        .step:not(:last-child):after { content:''; position:absolute; top:50%; left:100%; width:.5rem; border-top:1px solid rgba(148,163,184,.3); }
        .step-icon { display:block; font-size:1.05rem; margin-bottom:.25rem; }
        .step-label { color:#AEBBD0; font-size:.65rem; line-height:1.25; }
        .step-done { border-color:rgba(16,185,129,.4); background:rgba(16,185,129,.08); }
        .step-done .step-icon { color:var(--green); }
        .step-failed { border-color:rgba(239,68,68,.5); background:rgba(239,68,68,.1); }
        .step-failed .step-icon { color:var(--red); }
        .step-running { border-color:rgba(129,140,248,.7); background:rgba(99,102,241,.08); }
        .step-running .step-icon { color:#A5B4FC; }
        ::-webkit-scrollbar { width:8px; height:8px; }
        ::-webkit-scrollbar-track { background:#0B0F1A; }
        ::-webkit-scrollbar-thumb { background:#303B54; border-radius:8px; }
        @media (max-width:850px) { .block-container { padding:1rem 1rem 3rem; } .hero { padding:1.25rem; } .stepper { grid-template-columns:repeat(7,110px); } }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero() -> None:
    """Render a concise product heading."""
    st.markdown(
        """
        <section class="hero">
          <div class="hero-kicker">EXPENSE REPORTING</div>
          <h1 class="hero-title">Expense Report Agent</h1>
          <p class="hero-copy">Review, reconcile, and export business expenses from one workspace.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, icon: str, detail: str = "") -> None:
    """Render one compact dashboard metric."""
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-top">{escape(label)}<span class="material-symbols-rounded metric-icon">{escape(icon)}</span></div>
          <div class="metric-value">{escape(value)}</div>
          <div class="metric-detail">{escape(detail)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pipeline_stepper(steps: list[tuple[str, str]]) -> None:
    """Render a status-aware horizontal workflow stepper."""
    icons = {"done": "check_circle", "running": "progress_activity", "failed": "error", "pending": "radio_button_unchecked"}
    cards = []
    for label, status in steps:
        normalized = status if status in icons else "pending"
        cards.append(
            f'<div class="step step-{normalized}" aria-label="{escape(label)}: {escape(normalized)}">'
            f'<span class="material-symbols-rounded step-icon">{icons[normalized]}</span>'
            f'<span class="step-label">{escape(label)}</span></div>'
        )
    st.markdown(f'<div class="stepper">{"".join(cards)}</div>', unsafe_allow_html=True)
