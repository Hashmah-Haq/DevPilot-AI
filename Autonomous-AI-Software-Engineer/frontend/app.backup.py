
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Autonomous AI Software Engineer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session settings
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# Sidebar
with st.sidebar:
    st.markdown("## ◈ DevPilot AI")
    st.caption("AUTONOMOUS SOFTWARE ENGINEERING")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Code Workspace",
            "Agent Workflow",
            "Reports",
            "Settings"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.session_state.theme = st.selectbox(
        "Appearance",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    st.caption("Agentic AI + RAG • Python")

dark = st.session_state.theme == "Dark"

bg = "#0B1020" if dark else "#F6F8FC"
panel = "#151C30" if dark else "#FFFFFF"
text = "#F8FAFC" if dark else "#172033"
muted = "#94A3B8" if dark else "#64748B"
border = "#29344C" if dark else "#E2E8F0"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {text};
    }}
    [data-testid="stSidebar"] {{
        background-color: {panel};
    }}
    .block-container {{
        padding-top: 2rem;
        max-width: 1350px;
    }}
    .hero {{
        background: linear-gradient(
            120deg, #312E81 0%, #1E1B4B 100%
        );
        border: 1px solid #4F46E5;
        border-radius: 18px;
        padding: 28px;
        color: #FFFFFF;
        margin-bottom: 22px;
    }}
    .hero h1 {{
        color: #FFFFFF;
        margin-bottom: 8px;
        font-size: 2rem;
    }}
    .hero p {{
        color: #C7D2FE;
        margin-bottom: 0;
    }}
    .metric-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
    }}
    .metric-card h3 {{
        color: {muted};
        font-size: 14px;
        font-weight: 500;
        margin: 0 0 12px;
    }}
    .metric-card h2 {{
        color: {text};
        font-size: 28px;
        margin: 0;
    }}
    .section-card {{
        background: {panel};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 20px;
        margin-top: 14px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard
if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <h1>Autonomous AI Software Engineer</h1>
            <p>
                Analyze Python code, discover issues,
                generate AI fixes and review verification results.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Workspace Overview")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Analyses This Session",
         len(st.session_state.analysis_history)),
        ("Available Agent Modules", "4"),
        ("AI Model", "Qwen 2.5"),
        ("RAG Engine", "FAISS")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4], metrics
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h3>{label}</h3>
                    <h2>{value}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### AI Capabilities")

    a, b = st.columns(2)

    with a:
        st.markdown(
            """
            <div class="section-card">
                <h3>Code Intelligence</h3>
                <p>Syntax checking, Ruff analysis,
                Bandit security findings and AI fixes.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:
        st.markdown(
            """
            <div class="section-card">
                <h3>Agentic Workflow</h3>
                <p>Task planning, code review,
                RAG explanations and verification.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Dashboard preview is ready. "
        "Backend integration will be added next."
    )

# Code Workspace
elif page == "AI Code Workspace":
    st.title("AI Code Workspace")
    st.caption("Analyze, explain and improve Python code.")

    request = st.text_input(
        "What should the AI do?",
        value="Review this Python code and suggest fixes."
    )

    code = st.text_area(
        "Python Code",
        value=(
            "def add(a, b):\n"
            "    return a + b\n\n"
            "print(undefined_variable)"
        ),
        height=280
    )

    if st.button(
        "Run AI Analysis",
        type="primary",
        use_container_width=True
    ):
        st.info(
            "Frontend preview only. "
            "AI backend connection is coming next."
        )

    st.markdown("### Analysis Results")
    st.caption("Results will appear here after integration.")

# Agent Workflow
elif page == "Agent Workflow":
    st.title("Multi-Agent Workflow")
    st.caption("How our AI engineering agents collaborate.")

    steps = [
        "1. Task Planner",
        "2. Code Review Agent",
        "3. RAG Explanation Agent",
        "4. AI Fix Agent",
        "5. Static Verification",
        "6. Final Report"
    ]

    for step in steps:
        st.markdown(f"**{step}**")
        st.progress(0)

    st.caption(
        "Workflow visualization preview. "
        "Live execution tracking is not connected yet."
    )

# Reports
elif page == "Reports":
    st.title("Analysis Reports")

    reports_folder = (
        Path(__file__).resolve().parents[1] / "reports"
    )

    if reports_folder.exists():
        reports = sorted(
            reports_folder.glob("*.json"),
            reverse=True
        )

        if reports:
            selected = st.selectbox(
                "Select report",
                reports,
                format_func=lambda p: p.name
            )

            st.download_button(
                "Download JSON Report",
                data=selected.read_bytes(),
                file_name=selected.name,
                mime="application/json"
            )
        else:
            st.info("No reports generated yet.")
    else:
        st.info("Reports folder not found.")

# Settings
elif page == "Settings":
    st.title("Application Settings")

    st.write("Theme:", st.session_state.theme)
    st.write("AI Model: Qwen/Qwen2.5-0.5B-Instruct")
    st.write("RAG: FAISS + Sentence Transformers")
    st.write("Framework: Streamlit")
    st.caption("Backend configuration is read-only here.")
