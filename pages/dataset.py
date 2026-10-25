"""
Page 10: Dataset & Knowledge Provenance.
Displays external dataset sourcing, automated Kaggle downloader status, preprocessing audit,
and clearly articulates the distinction between benchmark data and symbolic medical knowledge.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from config import (
    DISCLAIMER_SHORT,
    KAGGLE_DATASET,
    EXTERNAL_DATASET_SOURCE_URL,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    BENCHMARK_DATA_DIR,
)
from src.kaggle_downloader import KaggleDownloader
from src.preprocessing import DataPreprocessor
from src.data_loader import DataLoader


def render_dataset_page():
    st.markdown("## Dataset & Knowledge Provenance")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    # Core Academic Differentiation Callout
    st.markdown(
        """
        <div style='background:#EFF6FF; border:1px solid #BFDBFE; border-radius:8px; padding:16px; margin-bottom:20px;'>
        <h4 style='color:#1E3A8A; margin:0;'>Academic Core Concept: Data vs. Knowledge vs. Reasoning</h4>
        <ul style='color:#1E40AF; margin-top:8px; margin-bottom:0;'>
            <li><b>DATA (= Benchmark Instances)</b>: External dataset records used strictly to evaluate, validate, and benchmark algorithmic scalability. No ML model training is performed.</li>
            <li><b>KNOWLEDGE (= Explicit Rules)</b>: Sourced strictly from authoritative clinical guidelines (WHO, CDC, NHS, Mayo Clinic).</li>
            <li><b>REASONING (= Classical AI)</b>: Forward Chaining, Backward Chaining, and Simple Matching reasoning over facts.</li>
            <li><b>OPTIMIZATION</b>: Domain-specific rule prioritization (specificity, evidence weight, relevance).</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    downloader = KaggleDownloader()
    preprocessor = DataPreprocessor()

    # Dataset Status Overview Cards
    is_raw_present = downloader.is_dataset_available_locally()
    report = DataLoader.get_preprocessing_report()
    is_processed = report is not None

    st.markdown("### Pipeline Status & External Kaggle Integration")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Kaggle Source", "Configured")
    with s2:
        st.metric("Raw Dataset", "Present (Cached)" if is_raw_present else "Missing")
    with s3:
        st.metric("Preprocessing Status", "Completed" if is_processed else "Pending")
    with s4:
        st.metric("Benchmark Cases", f"{report.get('processed_instances', 0)}" if report else "0")

    # Interactive Action Buttons
    st.markdown("### Interactive Dataset Operations")
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("Download Dataset via KaggleHub", use_container_width=True):
            with st.spinner("Executing secure Kaggle download..."):
                res = downloader.download()
                if res.get("success"):
                    st.success(res.get("message"))
                else:
                    st.warning(res.get("message"))
                    st.info(res.get("instructions"))
            st.rerun()

    with b2:
        if st.button("Execute Data Preprocessing Pipeline", use_container_width=True):
            with st.spinner("Normalizing tokens, handling missing values, and generating benchmark cases..."):
                try:
                    rep = preprocessor.run_pipeline()
                    st.success("Preprocessing pipeline completed successfully!")
                except Exception as e:
                    st.error(f"Preprocessing error: {e}")
            st.rerun()

    with b3:
        if st.button("Refresh Pipeline Status", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # Preprocessing Audit Report
    st.markdown("### Preprocessing Statistical Audit")
    if report:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f"""
                - **Configured Kaggle Dataset:** `{report.get('source')}`
                - **Mendeley Reference URL:** [{report.get('external_url')}]({report.get('external_url')})
                - **Raw File Evaluated:** `{report.get('raw_dataset_file')}`
                - **Raw Records (Rows):** `{report.get('raw_rows')}`
                - **Raw Columns:** `{report.get('raw_columns')}`
                - **Missing Values Handled:** `{report.get('raw_missing_values')}`
                """
            )
        with c2:
            st.markdown(
                f"""
                - **Processed Benchmark Instances:** `{report.get('processed_instances')}`
                - **Unique Diseases Represented:** `{report.get('unique_diseases_count')}`
                - **Unique Symptoms Vocabulary:** `{report.get('unique_symptoms_count')}`
                - **Average Symptoms per Instance:** `{report.get('average_symptoms_per_case')}`
                - **Symptom Range per Instance:** `{report.get('min_symptoms_per_case')} to {report.get('max_symptoms_per_case')}`
                """
            )

        # Dataset Preview
        st.markdown("### Processed Dataset Preview (Benchmark Cases)")
        df_processed = DataLoader.load_processed_data()
        if df_processed is not None:
            st.dataframe(df_processed.head(15), use_container_width=True)
    else:
        st.warning("Preprocessing has not yet been executed. Click 'Execute Data Preprocessing Pipeline' above.")
