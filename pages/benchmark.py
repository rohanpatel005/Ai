"""
Page 7: Benchmark Lab.
Conducts reproducible, empirical evaluations across test cases and knowledge base sizes
with real-time execution, Plotly visual analytics, and dataset exports.
"""

import streamlit as st
import pandas as pd
import json

from config import DISCLAIMER_SHORT, BENCHMARK_CASE_PRESETS, KB_SIZE_PRESETS, BENCHMARK_RESULTS_DIR
from src.knowledge_base import KnowledgeBase
from src.benchmark import BenchmarkEngine
from src.visualization import Visualizer


def render_benchmark_page():
    st.markdown("## Benchmark Lab & Experimental Scalability")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "**Empirical Benchmarking**: Measures real execution time, rules evaluated, rules fired, "
        "and inference iterations across genuine benchmark instances sourced from Kaggle. "
        "Strict academic integrity: No numbers or charts are fabricated."
    )

    kb = KnowledgeBase()
    benchmarker = BenchmarkEngine(kb)
    available_cases = len(benchmarker.cases)

    # Benchmark Controls Form
    with st.expander("Benchmark Configuration Controls", expanded=True):
        col_cases, col_kb, col_algos = st.columns([1, 1, 1])

        with col_cases:
            case_mode = st.radio("Number of Test Cases:", ["Preset", "Custom"], horizontal=True)
            if case_mode == "Preset":
                test_cases_count = st.selectbox("Select Preset:", [10, 25, 50, 100, 250, 500], index=1)
            else:
                test_cases_count = st.number_input("Enter Case Count:", min_value=1, max_value=max(10, available_cases), value=20)

        with col_kb:
            kb_mode = st.radio("Knowledge Base Size:", ["Preset", "Custom"], horizontal=True)
            if kb_mode == "Preset":
                kb_size_choice = st.selectbox("Select Rule Count:", ["Default (39)", 25, 50, 100, 250])
                kb_size = None if kb_size_choice == "Default (39)" else int(kb_size_choice)
            else:
                kb_size = st.number_input("Custom KB Size:", min_value=5, max_value=500, value=50)

        with col_algos:
            st.markdown("**Select Reasoning Paradigms:**")
            run_simple = st.checkbox("Simple Matching (Baseline)", value=True)
            run_forward = st.checkbox("Forward Chaining", value=True)
            run_backward = st.checkbox("Backward Chaining", value=True)
            run_prioritized = st.checkbox("Prioritized Forward Chaining", value=True)

        selected_algos = []
        if run_simple:
            selected_algos.append("Simple Matching (Baseline)")
        if run_forward:
            selected_algos.append("Forward Chaining")
        if run_backward:
            selected_algos.append("Backward Chaining")
        if run_prioritized:
            selected_algos.append("Prioritized Forward Chaining")

        run_btn = st.button("RUN BENCHMARK", type="primary", use_container_width=True)

    # State preservation for benchmark results
    if run_btn:
        if not selected_algos:
            st.error("Please select at least one algorithm to benchmark.")
        else:
            with st.spinner(f"Executing real benchmark across {test_cases_count} cases..."):
                benchmark_results = benchmarker.run_benchmark(
                    test_case_count=test_cases_count,
                    kb_size=kb_size,
                    selected_algorithms=selected_algos,
                )
                st.session_state["latest_benchmark"] = benchmark_results
            st.success("Benchmark completed successfully!")

    # Display Results
    if "latest_benchmark" in st.session_state:
        results = st.session_state["latest_benchmark"]
        df_summary = results["summary_df"]
        df_detailed = results["detailed_df"]

        st.markdown("### Empirical Benchmark Results")
        st.markdown(f"**Total Benchmark Execution Time:** `{results['total_time_ms']:.2f} ms`")

        # Summary Table
        st.dataframe(df_summary, use_container_width=True)

        # Plotly Visual Analytics
        st.markdown("### Visual Performance Comparison (Plotly)")
        fig_runtime = Visualizer.plot_benchmark_runtimes(df_summary)
        st.plotly_chart(fig_runtime, use_container_width=True)

        # Detailed per-case drilldown
        with st.expander("Inspect Detailed Per-Case Results"):
            st.dataframe(df_detailed, use_container_width=True, height=300)

        # Downloads
        st.markdown("### Export Real Benchmark Data")
        d1, d2 = st.columns(2)
        with d1:
            csv_data = df_summary.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Benchmark Summary (CSV)",
                data=csv_data,
                file_name="benchmark_summary.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with d2:
            json_str = json.dumps(results["summary_rows"], indent=2).encode("utf-8")
            st.download_button(
                "Download Benchmark Summary (JSON)",
                data=json_str,
                file_name="benchmark_summary.json",
                mime="application/json",
                use_container_width=True,
            )

    else:
        # Check if there is an existing benchmark file on disk
        latest_csv = BENCHMARK_RESULTS_DIR / "latest_benchmark_summary.csv"
        if latest_csv.exists():
            df_disk = pd.read_csv(latest_csv)
            st.markdown("### Most Recent Saved Benchmark Run")
            st.dataframe(df_disk, use_container_width=True)
            fig_disk = Visualizer.plot_benchmark_runtimes(df_disk)
            st.plotly_chart(fig_disk, use_container_width=True)
        else:
            st.info("Benchmark not run yet. Configure the controls above and click 'RUN BENCHMARK' to execute.")
