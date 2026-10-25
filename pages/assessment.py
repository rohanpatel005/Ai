"""
Page 2: Symptom Assessment & Input Formulation.
Provides search, multi-selection, custom/unseen symptom inputs, demo case loaders, and working memory validation.
"""

import streamlit as st
from typing import List

from config import DISCLAIMER_SHORT
from src.data_loader import DataLoader
from src.knowledge_base import KnowledgeBase


DEMO_CASES = {
    "Case 1: Typical Respiratory (Multi-Hop Proof)": {
        "symptoms": ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"],
        "description": "Standard multi-hop deduction: forms upper_respiratory_syndrome then deduces common_cold.",
    },
    "Case 2: Acute Lower Respiratory Consolidation": {
        "symptoms": ["high_fever", "cough", "breathlessness", "chest_pain", "phlegm", "fast_heart_rate"],
        "description": "Severe lower respiratory tract involvement pointing toward pneumonia.",
    },
    "Case 3: Insufficient Symptoms (Sparse Premise)": {
        "symptoms": ["fever"],
        "description": "Only an isolated constitutional symptom; tests safe handling of sparse input.",
    },
    "Case 4: Multi-Hypothesis Conflict / Differential": {
        "symptoms": ["fever", "fatigue", "headache"],
        "description": "Satisfies multiple competing rule premises (viral_fever vs systemic_fatigue).",
    },
    "Case 5: No Matching Rule (Knowledge Gap)": {
        "symptoms": ["sunken_eyes", "restlessness"],
        "description": "Valid clinical tokens that lack a corresponding complete rule premise in the KB.",
    },
    "Case 6: Target Hypothesis Proof (Backward Chaining)": {
        "symptoms": ["chills", "vomiting", "high_fever", "sweating", "headache"],
        "description": "Classic febrile paroxysm cluster suitable for backward proving of malaria.",
    },
    "Case 7: Cycle Detection Viva Demo": {
        "symptoms": ["fever_alpha"],
        "description": "Intentional circular dependency loop (fever_alpha -> beta -> gamma -> alpha) for viva demonstration.",
    },
    "Case 8: Custom Tropical Arbovirus Scenario": {
        "symptoms": ["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache"],
        "description": "Severe arthralgia and exanthem cluster establishing dengue_fever.",
    },
}


def render_assessment_page():
    st.markdown("## Symptom Assessment & Fact Formulation")
    st.caption(f"Course ECSCT24301 - Foundation of AI | {DISCLAIMER_SHORT}")

    st.info(
        "**Classical AI Principle**: Initial user symptoms become the **Initial State** (working memory facts). "
        "The inference engine evaluates these facts against explicit IF-THEN rules to deduce new facts and terminal hypotheses."
    )

    # Initialize session state for symptoms
    if "selected_symptoms" not in st.session_state:
        st.session_state.selected_symptoms = ["fever", "cough", "sore_throat"]

    kb = KnowledgeBase()
    known_symptoms = kb.get_all_conditions()
    dataset_symptoms = DataLoader.get_all_symptoms()
    combined_vocab = sorted(list(set(known_symptoms + dataset_symptoms)))

    # Demo Presets Section
    st.markdown("### Predefined Demonstration Scenarios (Viva Mode)")
    col_demo, col_desc = st.columns([1, 2])
    with col_demo:
        demo_choice = st.selectbox("Select a benchmark case:", list(DEMO_CASES.keys()))
    with col_desc:
        case_info = DEMO_CASES[demo_choice]
        st.markdown(f"**Description:** {case_info['description']}")
        st.markdown(f"**Case Symptoms:** `{', '.join(case_info['symptoms'])}`")
        if st.button("Load This Case Into Working Memory", use_container_width=True):
            st.session_state.selected_symptoms = list(case_info["symptoms"])
            st.rerun()

    st.markdown("---")

    # Interactive Symptom Picker
    st.markdown("### Interactive Symptom Selection")
    st.write("Search and select from the verified medical vocabulary, or add custom unseen symptoms:")

    col_picker, col_custom = st.columns([2, 1])

    with col_picker:
        current_selection = [s for s in st.session_state.selected_symptoms if s in combined_vocab]
        selected = st.multiselect(
            "Select symptoms from knowledge base & dataset vocabulary:",
            options=combined_vocab,
            default=current_selection,
            key="vocab_multiselect",
        )
        # Update session state with multiselect
        # Preserving custom symptoms not in multiselect
        custom_symptoms = [s for s in st.session_state.selected_symptoms if s not in combined_vocab]
        st.session_state.selected_symptoms = list(set(selected + custom_symptoms))

    with col_custom:
        st.markdown("**Add Custom / Unseen Symptom**")
        custom_input = st.text_input(
            "Enter arbitrary symptom token:",
            placeholder="e.g. loss_of_taste",
            help="Allows demonstration on unseen inputs as required by academic guidelines.",
        )
        if st.button("Add Custom Symptom", use_container_width=True):
            token = custom_input.strip().lower().replace(" ", "_")
            if token and token not in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.append(token)
                st.success(f"Added custom symptom: `{token}`")
                st.rerun()

    # Active Working Memory Display
    st.markdown("### Current Active Working Memory (Initial State)")
    if st.session_state.selected_symptoms:
        st.markdown("The following facts currently constitute the **Initial State** for reasoning:")
        cols = st.columns(min(6, max(1, len(st.session_state.selected_symptoms))))
        for idx, sym in enumerate(st.session_state.selected_symptoms):
            with cols[idx % len(cols)]:
                is_known = sym in known_symptoms
                badge_type = "Verified" if is_known else "Custom"
                st.markdown(
                    f"<div style='background:#F1F5F9; border-radius:8px; padding:10px; margin-bottom:8px; border-left:4px solid {'#2563EB' if is_known else '#F59E0B'};'>"
                    f"<b>{sym}</b><br><small style='color:#64748B;'>{badge_type}</small></div>",
                    unsafe_allow_html=True,
                )
    else:
        st.warning("Working memory is currently empty. Please select or enter at least one symptom.")

    # Action Bar
    st.markdown("---")
    act_col1, act_col2, act_col3 = st.columns([1, 1, 1])

    with act_col1:
        if st.button("Clear All Symptoms", use_container_width=True):
            st.session_state.selected_symptoms = []
            st.rerun()

    with act_col2:
        if st.button("Proceed to AI Reasoning", type="primary", use_container_width=True):
            st.session_state["nav_target"] = "AI Reasoning"
            st.rerun()

    with act_col3:
        if st.button("Run Full Algorithm Comparison", use_container_width=True):
            st.session_state["nav_target"] = "Compare Algorithms"
            st.rerun()
