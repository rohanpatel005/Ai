"""
Page 3: AI Reasoning & Explanation Engine.
Executes selected reasoning algorithm, displays live metrics, collapsible reasoning traces,
and WHY / HOW explanations.
"""

import streamlit as st
import pandas as pd

from config import DISCLAIMER_SHORT, DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA
from src.knowledge_base import KnowledgeBase
from src.rule_engine import RuleEngine
from src.explanation_engine import ExplanationEngine
from src.conflict_resolution import ConflictResolver
from src.cycle_detection import CycleDetector


def render_reasoning_page():
    st.markdown("## AI Inference Engine & Explainability")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    if "selected_symptoms" not in st.session_state or not st.session_state.selected_symptoms:
        st.warning("No symptoms in working memory! Please select symptoms on the Symptom Assessment page.")
        if st.button("Go to Symptom Assessment"):
            st.session_state["nav_target"] = "Symptom Assessment"
            st.rerun()
        return

    symptoms = st.session_state.selected_symptoms

    # Top Control Bar
    st.markdown("### Reasoning Paradigm Configuration")
    col_algo, col_kb_type = st.columns([2, 1])

    with col_algo:
        algorithm = st.selectbox(
            "Select AI Reasoning Paradigm:",
            [
                "Forward Chaining",
                "Prioritized Forward Chaining",
                "Backward Chaining",
                "Simple Matching (Baseline)",
            ],
            help="Select classical AI algorithm to reason over active facts.",
        )

    with col_kb_type:
        use_cyclic_demo = st.checkbox(
            "Inject Circular Rules (Viva Cycle Demo)",
            value=False,
            help="Injects cyclic rules A->B->C->A to demonstrate safe cycle termination.",
        )

    # Hyperparameter controls for Prioritized Forward Chaining
    alpha = DEFAULT_ALPHA
    beta = DEFAULT_BETA
    gamma = DEFAULT_GAMMA

    if algorithm == "Prioritized Forward Chaining":
        st.markdown("#### Rule Prioritization Hyperparameters")
        st.caption("priority = α × specificity + β × evidence_weight + γ × relevance")
        c_a, c_b, c_c = st.columns(3)
        with c_a:
            alpha = st.slider("α (Specificity Weight)", 0.0, 1.0, DEFAULT_ALPHA, 0.05)
        with c_b:
            beta = st.slider("β (Evidence Weight)", 0.0, 1.0, DEFAULT_BETA, 0.05)
        with c_c:
            gamma = st.slider("γ (Relevance Weight)", 0.0, 1.0, DEFAULT_GAMMA, 0.05)

    # Target hypothesis input for Backward Chaining
    target_hypothesis = None
    if algorithm == "Backward Chaining":
        kb = KnowledgeBase()
        conclusions = kb.get_all_conclusions()
        target_hypothesis = st.selectbox(
            "Select Target Hypothesis to Prove:",
            options=["[Auto-Detect Promising Targets]"] + conclusions,
            help="In Backward Chaining, reasoning works backward from a target goal to verify premises.",
        )
        if target_hypothesis == "[Auto-Detect Promising Targets]":
            target_hypothesis = None

    # Working Memory Preview
    st.markdown(f"**Current Input Symptoms:** `{', '.join(symptoms)}`")

    # Run Inference
    if use_cyclic_demo:
        active_kb = CycleDetector.create_viva_demonstration_cycle_kb()
    else:
        active_kb = KnowledgeBase()

    engine = RuleEngine(active_kb)
    result = engine.run_inference(
        algorithm=algorithm,
        symptoms=symptoms,
        target_hypothesis=target_hypothesis,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
    )

    st.markdown("---")

    # Live Cost Metrics Cards
    st.markdown("### Actual Execution Cost Metrics")
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.metric("Execution Time", f"{result.execution_time_ms:.2f} ms")
    with m_col2:
        st.metric("Rules Evaluated", result.evaluated_rules_count)
    with m_col3:
        st.metric("Rules Fired", len(result.fired_rules))
    with m_col4:
        st.metric("Iterations / Passes", result.iterations)
    with m_col5:
        st.metric("Inferred Facts", len(result.inferred_facts))

    # Inference Result & Status Banner
    st.markdown("### Inference Outcome")
    if result.cycle_detected:
        st.error(f"**SAFETY ALERT:** {result.status_message}")
    elif result.final_conclusion:
        st.success(
            f"**INFERENCE RESULT:** Based on the entered symptoms and knowledge rules, the system deduced: "
            f"**`{result.final_conclusion.upper()}`**"
        )
    else:
        st.warning(f"**RESULT:** {result.status_message}")

    # Conflict / Multi-Hypothesis Analysis
    conflict_report = ConflictResolver.analyze_conflicts(result)
    if conflict_report["has_conflict"]:
        st.warning(f"**DIFFERENTIAL DIAGNOSIS / CONFLICT DETECTED:** {conflict_report['message']}")
        st.info(conflict_report.get("safety_recommendation", ""))
        for item in conflict_report["differential_list"]:
            with st.expander(f"Hypothesis: {item['hypothesis'].upper()} (Evidence: {item['evidence_weight']})"):
                st.write(f"- **Supporting Rule IDs:** {', '.join(item['supporting_rule_ids'])}")
                st.write(f"- **Matched Premises:** {', '.join(item['matched_conditions'])}")
                st.write(f"- **Cited Sources:** {', '.join(item['sources'])}")

    # Formal Explanation Engine Section
    st.markdown("### Explanation Engine (WHY & HOW)")
    explanation = ExplanationEngine.generate_narrative_explanation(result)

    tab_why, tab_how, tab_trace = st.tabs(["Why Was This Result Deduced?", "How Did the Inference Chain Progress?", "Raw Step-by-Step Trace"])

    with tab_why:
        st.markdown("**Algorithmic Justification (WHY):**")
        st.markdown(f"*{explanation['what_summary']}*")
        for bullet in explanation["why_explanations"]:
            st.markdown(f"- {bullet}")

    with tab_how:
        st.markdown("**Causal Deduction Stages (HOW):**")
        for stage in explanation["how_chain_stages"]:
            st.markdown(
                f"<div style='background:#F8FAFC; border-left:4px solid #2563EB; padding:12px; margin-bottom:10px; border-radius:6px;'>"
                f"<b>Stage {stage['stage']}: {stage['title']}</b><br>{stage['content']}</div>",
                unsafe_allow_html=True,
            )

    with tab_trace:
        st.markdown("**Chronological Rule Evaluation Trace:**")
        df_trace = ExplanationEngine.get_steps_dataframe(result)
        st.dataframe(df_trace, use_container_width=True, height=350)

        # Download Trace Button
        csv_trace = df_trace.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Reasoning Trace (CSV)",
            data=csv_trace,
            file_name=f"reasoning_trace_{algorithm.replace(' ', '_').lower()}.csv",
            mime="text/csv",
        )
