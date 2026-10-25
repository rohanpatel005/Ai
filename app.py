"""
Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining.
Central Application Controller & AI Dashboard.
Course: ECSCT24301 - Foundation of AI, Adani University.
"""

import sys
from pathlib import Path
import streamlit as st

# Configure project root
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import (
    PROJECT_TITLE,
    APP_SHORT_TITLE,
    UNIVERSITY_NAME,
    FACULTY_NAME,
    DEPARTMENT_NAME,
    COURSE_CODE,
    COURSE_NAME,
    PROJECT_TRACK,
    DISCLAIMER_SHORT,
    DISCLAIMER_FULL,
    TEAM_MEMBERS,
)
from src.knowledge_base import KnowledgeBase
from src.data_loader import DataLoader

# Page Imports
from pages.assessment import render_assessment_page
from pages.reasoning import render_reasoning_page
from pages.backward import render_backward_page
from pages.comparison import render_comparison_page
from pages.knowledge_base import render_knowledge_base_page
from pages.benchmark import render_benchmark_page
from pages.error_analysis import render_error_analysis_page
from pages.methodology import render_methodology_page
from pages.dataset import render_dataset_page
from pages.about import render_about_page

# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{APP_SHORT_TITLE} | {UNIVERSITY_NAME}",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Professional AI Dashboard CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Top Safety Banner */
    .safety-banner {
        background: linear-gradient(90deg, #FEF2F2 0%, #FFFBEB 100%);
        border: 1px solid #FCA5A5;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #991B1B;
        font-size: 0.88rem;
        font-weight: 500;
    }

    /* Dashboard Header Card */
    .dashboard-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    /* Quick Action Card */
    .quick-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
    }
    .quick-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
        border-color: #3B82F6;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_dashboard_home():
    """Renders Page 1: Home Dashboard."""

    # Top Medical Safety Banner
    st.markdown(
        f"""
        <div class="safety-banner">
            <span style="font-size: 1.25rem;">⚠️</span>
            <div>
                <b>{DISCLAIMER_SHORT}</b><br>
                <span style="font-size: 0.8rem; color:#7F1D1D;">{DISCLAIMER_FULL}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Header Card
    st.markdown(
        f"""
        <div class="dashboard-header">
            <span style="background:#2563EB; color:white; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">
                {PROJECT_TRACK} • {COURSE_CODE}
            </span>
            <h1 style="color:white; margin:10px 0 6px 0; font-size:1.85rem; font-weight:700;">
                {PROJECT_TITLE}
            </h1>
            <p style="color:#94A3B8; margin:0; font-size:0.95rem;">
                {UNIVERSITY_NAME} | {FACULTY_NAME} | {DEPARTMENT_NAME}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # System Status Metrics
    kb = KnowledgeBase()
    report = DataLoader.get_preprocessing_report()
    rules_count = len(kb.rules)
    dataset_records = report.get("processed_instances", 4920) if report else 4920
    symptoms_count = report.get("unique_symptoms_count", 131) if report else 131

    st.markdown("### System Telemetry & Knowledge Engine Status")
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)

    with s_col1:
        st.metric(label="Knowledge Base Rules", value=rules_count, delta="Authoritative (WHO/CDC/NHS)")
    with s_col2:
        st.metric(label="Benchmark Dataset Cases", value=dataset_records, delta="Kaggle Sourced")
    with s_col3:
        st.metric(label="Symptom Vocabulary", value=symptoms_count, delta="Standardized Tokens")
    with s_col4:
        st.metric(label="Reasoning Paradigms", value="4 Implemented", delta="Pure Symbolic Logic")

    st.markdown("---")

    # Quick Navigation Cards
    st.markdown("### Modular Application Workspaces")
    row1_c1, row1_c2, row1_c3 = st.columns(3)

    with row1_c1:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">🩺 Symptom Assessment</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Formulate patient working memory facts. Search symptoms, add custom unseen tokens, or load 8 viva demonstration cases.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch Assessment", key="btn_dash_assessment", use_container_width=True):
            st.session_state["nav_target"] = "Symptom Assessment"
            st.rerun()

    with row1_c2:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">🧠 AI Reasoning</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Execute Forward, Backward, or Prioritized Forward Chaining with live WHY and HOW explanation breakdowns and execution traces.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Launch AI Reasoning", key="btn_dash_reasoning", use_container_width=True):
            st.session_state["nav_target"] = "AI Reasoning"
            st.rerun()

    with row1_c3:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">⚖️ Compare Algorithms</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Execute the same symptom input through all 4 algorithms simultaneously to compare execution time, rules fired, and iterations.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Compare All 4 Paradigms", key="btn_dash_comparison", use_container_width=True):
            st.session_state["nav_target"] = "Compare Algorithms"
            st.rerun()

    row2_c1, row2_c2, row2_c3 = st.columns(3)

    with row2_c1:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">🌲 Backward Explorer</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Select target clinical goals and visualize recursive sub-goal resolution with interactive Plotly proof tree DAGs.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Backward Tree", key="btn_dash_backward", use_container_width=True):
            st.session_state["nav_target"] = "Backward Chaining Explorer"
            st.rerun()

    with row2_c2:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">📊 Benchmark Lab</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Execute empirical batch runs on up to 500 test cases and 250 rules. Measure real latency and export CSV/JSON results.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Benchmark Lab", key="btn_dash_benchmark", use_container_width=True):
            st.session_state["nav_target"] = "Benchmark Lab"
            st.rerun()

    with row2_c3:
        st.markdown(
            """
            <div class="quick-card">
                <h4 style="margin:0 0 8px 0; color:#1E293B;">🛡️ Error & Failure Analysis</h4>
                <p style="color:#64748B; font-size:0.88rem; margin-bottom:12px;">
                    Test all 14 mandatory academic edge-case scenarios: cycle loops, missing knowledge, conflicts, and sparse inputs.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Audit 14 Edge Cases", key="btn_dash_errors", use_container_width=True):
            st.session_state["nav_target"] = "Error Analysis"
            st.rerun()

    st.markdown("---")

    # End-to-End PBL Pipeline Architecture Diagram
    st.markdown("### End-to-End Classical AI Reasoning Architecture")
    st.markdown(
        """
        ```
        +-----------------------------------------------------------------------------------------+
        |                               USER INPUT / BENCHMARK CASE                               |
        |              [Selected Symptoms: e.g. fever, cough, sore_throat, runny_nose]            |
        +-----------------------------------------------------------------------------------------+
                                                   |
                                                   v
        +-----------------------------------------------------------------------------------------+
        |                               WORKING MEMORY (FACT STATE)                               |
        |                         S_0 = {fever, cough, sore_throat, runny_nose}                   |
        +-----------------------------------------------------------------------------------------+
                                                   |
                          +------------------------+------------------------+
                          |                                                 |
                          v                                                 v
        +------------------------------------+            +---------------------------------------+
        |   KNOWLEDGE BASE (EXPLICIT RULES)  |            |        AI INFERENCE ENGINE            |
        |   - Cited WHO/CDC/NHS Clinical Rules|            |   1. Simple Symptom Matching Baseline |
        |   - Specificity, Priority, Weights  | --------> |   2. Data-Driven Forward Chaining     |
        |   - Multi-Hop Intermediate Rules   |            |   3. Goal-Driven Backward Chaining    |
        |   - Cycle-Free Directed Graph      |            |   4. Prioritized Forward Chaining     |
        +------------------------------------+            +---------------------------------------+
                                                                            |
                                                   +------------------------+
                                                   |
                                                   v
        +-----------------------------------------------------------------------------------------+
        |                      CYCLE DETECTION & CONFLICT RESOLUTION SUBSYSTEM                     |
        |   - Visited-Set Cycle Guard: Terminates recursive loops safely (A -> B -> C -> A)       |
        |   - Differential Diagnosis: Transparently outputs competing hypotheses without pruning   |
        +-----------------------------------------------------------------------------------------+
                                                   |
                                                   v
        +-----------------------------------------------------------------------------------------+
        |                           EXPLANATION & VISUALIZATION ENGINE                            |
        |   - WHY was rule fired? (Premise condition verification)                                |
        |   - HOW was deduction chained? (Initial facts -> Intermediate syndrome -> Diagnosis)     |
        |   - Interactive Plotly DAGs, Goal Trees, and Real Empirical Complexity Scalability     |
        +-----------------------------------------------------------------------------------------+
        ```
        """
    )


def main():
    # Sidebar Institutional & Navigation Section
    st.sidebar.markdown(f"### 🩺 {APP_SHORT_TITLE}")
    st.sidebar.caption(f"{UNIVERSITY_NAME} • {COURSE_CODE}")

    pages_list = [
        "Home Dashboard",
        "Symptom Assessment",
        "AI Reasoning",
        "Backward Chaining Explorer",
        "Compare Algorithms",
        "Knowledge Base Explorer",
        "Benchmark Lab",
        "Error Analysis",
        "Academic Methodology",
        "Dataset & Knowledge Provenance",
        "About & References",
    ]

    # Handle internal redirection if set
    default_index = 0
    if "nav_target" in st.session_state:
        target = st.session_state.pop("nav_target")
        if target in pages_list:
            default_index = pages_list.index(target)

    selected_page = st.sidebar.radio(
        "Navigation Menu:",
        options=pages_list,
        index=default_index,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 Student Project Team")
    for m in TEAM_MEMBERS:
        st.sidebar.markdown(f"**{m['name']}** (`{m['usn']}`)")

    st.sidebar.markdown("---")
    st.sidebar.caption("Adani University FEST • 2026")

    # Routing
    if selected_page == "Home Dashboard":
        render_dashboard_home()
    elif selected_page == "Symptom Assessment":
        render_assessment_page()
    elif selected_page == "AI Reasoning":
        render_reasoning_page()
    elif selected_page == "Backward Chaining Explorer":
        render_backward_page()
    elif selected_page == "Compare Algorithms":
        render_comparison_page()
    elif selected_page == "Knowledge Base Explorer":
        render_knowledge_base_page()
    elif selected_page == "Benchmark Lab":
        render_benchmark_page()
    elif selected_page == "Error Analysis":
        render_error_analysis_page()
    elif selected_page == "Academic Methodology":
        render_methodology_page()
    elif selected_page == "Dataset & Knowledge Provenance":
        render_dataset_page()
    elif selected_page == "About & References":
        render_about_page()


if __name__ == "__main__":
    main()
