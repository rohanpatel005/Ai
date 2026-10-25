"""
Page 5: Algorithm Comparison.
Simultaneously executes the same input across all 4 reasoning algorithms,
displaying side-by-side comparative metrics, interactive Plotly charts, and exportable tables.
"""

import streamlit as st
import pandas as pd

from config import DISCLAIMER_SHORT
from src.knowledge_base import KnowledgeBase
from src.rule_engine import RuleEngine
from src.visualization import Visualizer


def render_comparison_page():
    st.markdown("## Side-by-Side Algorithm Comparison")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "This evaluation executes the exact same working memory facts across all four reasoning approaches: "
        "Simple Symptom Matching (Baseline), Forward Chaining, Backward Chaining, and Prioritized Forward Chaining."
    )

    if "selected_symptoms" not in st.session_state or not st.session_state.selected_symptoms:
        st.session_state.selected_symptoms = ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"]

    symptoms = st.session_state.selected_symptoms
    st.markdown(f"**Active Input Symptoms:** `{', '.join(symptoms)}`")

    # Run all 4 algorithms live
    kb = KnowledgeBase()
    engine = RuleEngine(kb)
    results_map = engine.run_all_algorithms(symptoms)

    # Comparative Summary Table
    comparison_rows = []
    for name, res in results_map.items():
        comparison_rows.append({
            "Algorithm": name,
            "Conclusion": (res.final_conclusion or "None").upper(),
            "Execution Time (ms)": round(res.execution_time_ms, 3),
            "Rules Evaluated": res.evaluated_rules_count,
            "Rules Fired": len(res.fired_rules),
            "Inference Iterations": res.iterations,
            "Inferred Facts Count": len(res.inferred_facts),
            "Status": res.status_message,
        })

    df_comp = pd.DataFrame(comparison_rows)

    # High-level Metrics Grid
    st.markdown("### Comparative Performance Metrics")
    cols = st.columns(4)
    for idx, row in enumerate(comparison_rows):
        with cols[idx]:
            st.markdown(
                f"<div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px; margin-bottom:10px;'>"
                f"<b style='color:#1E293B;'>{row['Algorithm']}</b><br>"
                f"<small style='color:#64748B;'>Deduction:</small> <b>{row['Conclusion']}</b><br>"
                f"<small style='color:#64748B;'>Time:</small> <b>{row['Execution Time (ms)']} ms</b><br>"
                f"<small style='color:#64748B;'>Evaluated / Fired:</small> <b>{row['Rules Evaluated']} / {row['Rules Fired']}</b>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # Interactive Comparison Chart
    st.markdown("### Performance & Rule Evaluation Chart (Plotly)")
    fig = Visualizer.plot_algorithm_comparison(results_map)
    st.plotly_chart(fig, use_container_width=True)

    # Full Tabular Comparison
    st.markdown("### Comprehensive Comparative Table")
    st.dataframe(df_comp, use_container_width=True)

    # Download Comparison CSV
    csv_bytes = df_comp.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Algorithm Comparison (CSV)",
        data=csv_bytes,
        file_name="algorithm_comparison_results.csv",
        mime="text/csv",
    )

    # Academic Analysis & Viva Insights
    st.markdown("### Academic Insights for Student Viva")
    with st.expander("Why do these algorithmic differences occur?", expanded=True):
        st.markdown(
            """
            1. **Simple Matching vs. Forward Chaining**:
               - *Simple Matching (Baseline)* evaluates direct overlap with single-level rules. It cannot create multi-hop intermediate deductions (e.g. deduce `upper_respiratory_syndrome` and then use that to conclude `common_cold`).
               - *Forward Chaining* operates iteratively over working memory, chaining intermediate syndromes into final diagnoses.

            2. **Normal Forward Chaining vs. Prioritized Forward Chaining**:
               - *Prioritized Forward Chaining* sorts rules using dynamic specificity, evidence weight, and working memory relevance. On targeted or large knowledge bases, it fires the most specific and pertinent rules first.

            3. **Forward Chaining vs. Backward Chaining**:
               - *Forward Chaining* is **data-driven** (bottom-up): it starts with known facts and derives all logically reachable conclusions.
               - *Backward Chaining* is **goal-driven** (top-down): it starts with a target hypothesis and only evaluates rules necessary to verify that goal, pruning irrelevant knowledge branches.
            """
        )
