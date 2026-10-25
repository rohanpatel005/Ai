"""
Page 6: Knowledge Base Explorer & Rule Validation.
Search, filter, inspect, and export authoritative explicit IF-THEN rules with clinical citations.
"""

import streamlit as st
import pandas as pd
import json

from config import DISCLAIMER_SHORT, RULES_CSV_PATH, RULES_JSON_PATH
from src.knowledge_base import KnowledgeBase


def render_knowledge_base_page():
    st.markdown("## Medical Knowledge Base Explorer & Validation")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "**Knowledge Representation Principle**: In classical AI, the knowledge base is completely separate "
        "from the inference engine. Each rule is an explicit IF-THEN production rule with verified clinical source citations."
    )

    kb = KnowledgeBase()
    val = kb.validate()

    # Validation Status Banner
    st.markdown("### Knowledge Base Formal Integrity Status")
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    with v_col1:
        st.metric("Total Rules", val.rule_count)
    with v_col2:
        st.metric("Unique Premises / Symptoms", val.unique_conditions_count)
    with v_col3:
        st.metric("Unique Conclusions", val.unique_conclusions_count)
    with v_col4:
        st.metric("Integrity Check", "PASSED (No Errors)" if val.is_valid else "FAILED")

    if not val.is_valid:
        st.error(f"Rule Validation Errors Found: {val.errors}")

    st.markdown("---")

    # Interactive Search and Filters
    st.markdown("### Search & Filter Rules")
    f_col1, f_col2, f_col3 = st.columns(3)

    rules = kb.get_all_rules()
    all_conclusions = ["All"] + kb.get_all_conclusions()
    all_conditions = ["All"] + kb.get_all_conditions()

    with f_col1:
        search_query = st.text_input("Search (Rule ID, description, or keyword):", placeholder="e.g. malaria, fever, R_RESP")
    with f_col2:
        filter_conclusion = st.selectbox("Filter by Conclusion / Diagnosis:", all_conclusions)
    with f_col3:
        filter_condition = st.selectbox("Filter by Required Symptom / Premise:", all_conditions)

    # Filter logic
    filtered_rules = []
    q_lower = search_query.strip().lower()

    for r in rules:
        if q_lower:
            match_id = q_lower in r.rule_id.lower()
            match_desc = q_lower in r.description.lower()
            match_conc = q_lower in r.conclusion.lower()
            match_cond = any(q_lower in c.lower() for c in r.conditions)
            if not (match_id or match_desc or match_conc or match_cond):
                continue

        if filter_conclusion != "All" and r.conclusion != filter_conclusion:
            continue

        if filter_condition != "All" and filter_condition not in r.conditions:
            continue

        filtered_rules.append(r)

    st.markdown(f"**Showing {len(filtered_rules)} of {len(rules)} rules:**")

    # Display Table
    table_rows = []
    for r in filtered_rules:
        table_rows.append({
            "Rule ID": r.rule_id,
            "Conclusion": r.conclusion,
            "Premises (IF)": ", ".join(r.conditions),
            "Evidence Weight": r.evidence_weight,
            "Specificity": r.specificity,
            "Priority": r.priority,
            "Clinical Source": r.source,
        })
    df_rules = pd.DataFrame(table_rows)
    st.dataframe(df_rules, use_container_width=True, height=350)

    # Rule Deep-Dive Inspector
    st.markdown("### Detailed Rule Inspector")
    if filtered_rules:
        rule_ids = [r.rule_id for r in filtered_rules]
        selected_id = st.selectbox("Select Rule to Inspect Full Clinical Metadata:", rule_ids)
        selected_rule = kb.get_rule_by_id(selected_id)

        if selected_rule:
            with st.container():
                st.markdown(
                    f"<div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:16px;'>"
                    f"<h4 style='margin:0; color:#1E293B;'>Rule {selected_rule.rule_id}: IF {', '.join(selected_rule.conditions)} THEN {selected_rule.conclusion}</h4>"
                    f"<p style='color:#475569; margin-top:8px;'>{selected_rule.description}</p>"
                    f"<table style='width:100%; border-collapse:collapse; margin-top:8px;'>"
                    f"<tr><td><b>Evidence Weight:</b></td><td>{selected_rule.evidence_weight}</td><td><b>Specificity (Premise Count):</b></td><td>{selected_rule.specificity}</td></tr>"
                    f"<tr><td><b>Static Priority:</b></td><td>{selected_rule.priority}</td><td><b>Medical Source:</b></td><td>{selected_rule.source}</td></tr>"
                    f"<tr><td colspan='4'><b>Authoritative Source URL:</b> <a href='{selected_rule.source_url}' target='_blank'>{selected_rule.source_url}</a></td></tr>"
                    f"</table>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # Downloads Section
    st.markdown("---")
    st.markdown("### Export Knowledge Base")
    d_col1, d_col2 = st.columns(2)

    with d_col1:
        if RULES_CSV_PATH.exists():
            with open(RULES_CSV_PATH, "rb") as f:
                st.download_button(
                    "Download Knowledge Base (CSV)",
                    data=f.read(),
                    file_name="medical_rules.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    with d_col2:
        if RULES_JSON_PATH.exists():
            with open(RULES_JSON_PATH, "rb") as f:
                st.download_button(
                    "Download Knowledge Base (JSON)",
                    data=f.read(),
                    file_name="medical_rules.json",
                    mime="application/json",
                    use_container_width=True,
                )
