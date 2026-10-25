"""
Page 8: Error and Failure Analysis.
Evaluates all 14 academic failure-mode scenarios verifying safe termination,
cycle detection, conflict resolution, and graceful exception handling.
"""

import streamlit as st
import pandas as pd

from config import DISCLAIMER_SHORT
from src.evaluation import ErrorAnalyzer


def render_error_analysis_page():
    st.markdown("## Error & Failure Mode Analysis")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "**Robustness & Safety Principle**: A critical requirement of an AI expert system is safe and predictable "
        "handling of edge cases, conflicting goals, cyclic loops, and out-of-vocabulary inputs without crashing."
    )

    analyzer = ErrorAnalyzer()
    scenarios = analyzer.SCENARIOS

    # Top Control: Single vs Batch Run
    st.markdown("### Interactive Failure-Mode Evaluator")
    mode = st.radio("Evaluation Mode:", ["Single Scenario Deep-Dive", "Run All 14 Scenarios (Batch Audit)"], horizontal=True)

    if mode == "Single Scenario Deep-Dive":
        scenario_titles = [f"Scenario {s['id']}: {s['title']}" for s in scenarios]
        selected_title = st.selectbox("Select Scenario to Inspect & Execute:", scenario_titles)
        selected_id = int(selected_title.split(":")[0].replace("Scenario", "").strip())

        with st.spinner(f"Executing Scenario #{selected_id}..."):
            result = analyzer.run_scenario(selected_id)

        st.markdown("---")
        status_color = "#10B981" if result["passed"] else "#EF4444"
        badge_text = "PASSED (Safe Handling)" if result["passed"] else "FAILED"

        st.markdown(
            f"<div style='background:#F8FAFC; border-left:6px solid {status_color}; border-radius:8px; padding:16px; margin-bottom:15px;'>"
            f"<h3 style='margin:0; color:#1E293B;'>{result['title']}</h3>"
            f"<p style='color:#64748B; margin-top:4px;'>{result['description']}</p>"
            f"<span style='background:{status_color}; color:white; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:12px;'>{badge_text}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Test Inputs Supplied:**")
            st.code(str(result["inputs"]))
            st.markdown("**Expected Academic Behavior:**")
            st.info(result["expected_behavior"])

        with c2:
            st.markdown("**Actual System Execution Output:**")
            st.success(result["actual_behavior"])
            st.markdown("**Inference Status Message:**")
            st.write(f"`{result['status_message']}`")

        # Summary of inference metrics for this scenario
        with st.expander("Inspect Execution Metrics for this Scenario"):
            st.json(result["result_summary"])

        if result["conflict_analysis"]["has_conflict"]:
            st.warning("**Conflict Resolution Triggered:**")
            st.json(result["conflict_analysis"])

    else:
        # Batch Audit Mode
        if st.button("RUN COMPLETE 14-SCENARIO AUDIT", type="primary", use_container_width=True):
            with st.spinner("Executing all 14 failure-mode tests..."):
                all_results = analyzer.run_all_scenarios()
                st.session_state["batch_error_results"] = all_results
            st.success("14-Scenario audit completed successfully!")

        if "batch_error_results" in st.session_state:
            audit = st.session_state["batch_error_results"]
            passed_count = sum(1 for r in audit if r["passed"])

            st.markdown(f"### Audit Summary: {passed_count} / {len(audit)} Scenarios Passed")

            rows = []
            for r in audit:
                rows.append({
                    "ID": r["id"],
                    "Scenario": r["title"],
                    "Inputs": str(r["inputs"]),
                    "Status": "PASSED" if r["passed"] else "FAILED",
                    "Actual Behavior": r["actual_behavior"],
                })

            df_audit = pd.DataFrame(rows)
            st.dataframe(df_audit, use_container_width=True, height=450)

            # Download Audit Report CSV
            csv_audit = df_audit.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Complete Error Analysis Audit (CSV)",
                data=csv_audit,
                file_name="error_analysis_audit.csv",
                mime="text/csv",
            )
