"""
Page 4: Backward Chaining Goal Tree Explorer.
Visualizes goal-driven deduction, recursive sub-goal resolution, visited-set cycle detection,
and proof trees.
"""

import streamlit as st

from config import DISCLAIMER_SHORT
from src.knowledge_base import KnowledgeBase
from src.backward_chaining import BackwardChainingEngine
from src.visualization import Visualizer
from src.models import BackwardGoalNode


def render_node_markdown(node: BackwardGoalNode, indent: int = 0):
    """Recursively formats a BackwardGoalNode as structured markdown."""
    indent_space = "&nbsp;" * (indent * 6)
    icon_map = {
        "PROVEN_FACT": "🟢 [PROVEN FACT]",
        "PROVEN_RULE": "🔵 [PROVEN RULE]",
        "FAILED": "🔴 [FAILED]",
        "CYCLE_DETECTED": "⛔ [CYCLE DETECTED]",
        "EVALUATING": "🟡 [EVALUATING]",
        "ROOT": "🟣 [GOAL EXPLORATION]",
    }
    icon = icon_map.get(node.status, "⚪")
    rule_str = f" <i>via {node.rule_id}</i>" if node.rule_id else ""
    st.markdown(
        f"{indent_space}{icon} <b>{node.goal}</b>{rule_str} — <small style='color:#64748B;'>{node.message}</small>",
        unsafe_allow_html=True,
    )
    for child in node.children:
        render_node_markdown(child, indent + 1)


def render_backward_page():
    st.markdown("## Backward Chaining Goal Tree Explorer")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "**Backward Chaining (Goal-Driven Reasoning)** starts with a clinical target hypothesis, "
        "finds rules concluding that hypothesis, and recursively attempts to prove all premise conditions "
        "against known working memory facts or secondary sub-goals."
    )

    if "selected_symptoms" not in st.session_state or not st.session_state.selected_symptoms:
        st.session_state.selected_symptoms = ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"]

    symptoms = st.session_state.selected_symptoms
    kb = KnowledgeBase()
    conclusions = kb.get_all_conclusions()

    # Controls
    col_target, col_symptoms = st.columns([1, 1])
    with col_target:
        target = st.selectbox(
            "Select Target Hypothesis to Establish:",
            options=conclusions,
            index=conclusions.index("common_cold") if "common_cold" in conclusions else 0,
        )

    with col_symptoms:
        st.markdown(f"**Known Symptom Facts in Memory:**")
        st.write(f"`{', '.join(symptoms)}`")

    # Run Backward Chaining Engine
    engine = BackwardChainingEngine(kb)
    result = engine.infer(initial_facts=symptoms, target_hypothesis=target)

    st.markdown("---")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Target Goal", target)
    with m2:
        is_proven = bool(result.supported_hypotheses and result.supported_hypotheses[0].hypothesis == target)
        status_label = "PROVEN" if is_proven else "UNPROVEN"
        st.metric("Proof Status", status_label)
    with m3:
        st.metric("Rules Evaluated", result.evaluated_rules_count)
    with m4:
        st.metric("Proof Time", f"{result.execution_time_ms:.2f} ms")

    # Interactive Goal Tree Visualization
    st.markdown("### Interactive Goal Resolution Tree (Plotly DAG)")
    if result.backward_tree:
        fig = Visualizer.render_backward_tree_graph(result.backward_tree)
        st.plotly_chart(fig, use_container_width=True)

    # Hierarchical Proof Trace
    st.markdown("### Hierarchical Recursive Sub-Goal Breakdown")
    with st.expander("Expand Sub-Goal Proof Hierarchy", expanded=True):
        if result.backward_tree:
            render_node_markdown(result.backward_tree)

    # Detailed Step Trace
    with st.expander("Chronological Backward Proof Steps"):
        trace_data = []
        for s in result.trace:
            trace_data.append({
                "Step": s.step_number,
                "Sub-Goal / Rule": s.rule_id,
                "Conditions Evaluated": ", ".join(s.conditions_evaluated),
                "Status": "PROVEN" if s.fired else "FAILED",
                "Reason": s.reason,
            })
        st.table(trace_data)
