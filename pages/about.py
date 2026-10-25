"""
Page 11: Institutional Metadata, Team, and Verified APA References.
Presents university details, student team roles, verified APA citations, and safety disclosures.
"""

import streamlit as st

from config import (
    DISCLAIMER_FULL,
    UNIVERSITY_NAME,
    FACULTY_NAME,
    DEPARTMENT_NAME,
    COURSE_CODE,
    COURSE_NAME,
    PROJECT_TRACK,
    PROJECT_TITLE,
    TEAM_MEMBERS,
)


def render_about_page():
    st.markdown("## Academic Project Details & References")
    st.caption(f"{UNIVERSITY_NAME} | {FACULTY_NAME}")

    # Institutional Metadata Card
    st.markdown(
        f"""
        <div style='background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:18px; margin-bottom:20px;'>
        <h3 style='color:#1E293B; margin:0;'>{PROJECT_TITLE}</h3>
        <p style='color:#475569; margin:4px 0 12px 0;'><b>Course:</b> {COURSE_CODE} – {COURSE_NAME} | <b>Track:</b> {PROJECT_TRACK}</p>
        <table style='width:100%; border-collapse:collapse; color:#334155;'>
            <tr><td><b>University:</b></td><td>{UNIVERSITY_NAME}</td><td><b>Faculty:</b></td><td>{FACULTY_NAME}</td></tr>
            <tr><td><b>Department:</b></td><td>{DEPARTMENT_NAME}</td><td><b>Academic Year:</b></td><td>2026</td></tr>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Student Team Section
    st.markdown("### Student Project Team")
    cols = st.columns(len(TEAM_MEMBERS))
    for idx, member in enumerate(TEAM_MEMBERS):
        with cols[idx]:
            st.markdown(
                f"""
                <div style='background:#FFFFFF; border:1px solid #CBD5E1; border-top:4px solid #2563EB; border-radius:8px; padding:14px; text-align:center;'>
                <h4 style='margin:0; color:#1E293B;'>{member['name']}</h4>
                <p style='color:#2563EB; font-weight:bold; margin:4px 0;'>USN: {member['usn']}</p>
                <small style='color:#64748B;'>{member['role']}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Technology Stack
    st.markdown("### Technology Stack")
    st.markdown(
        """
        - **Core Logic & AI Reasoning**: Python 3.14 (Pure symbolic implementation of Forward Chaining, Backward Chaining, and Rule Prioritization)
        - **Interactive UI Framework**: Streamlit (Multi-page architecture, session state, custom CSS)
        - **Data Handling & Caching**: Pandas, NumPy
        - **Data Visualization & DAGs**: Plotly Express, Plotly Graph Objects
        - **Graph & Cycle Detection**: NetworkX (Directed cycle analysis, visited-set proof trees)
        - **Dataset Ingestion**: KaggleHub (Official authenticated Kaggle API SDK)
        - **Automated Unit Testing**: Pytest
        """
    )

    st.markdown("---")

    # Verified APA References
    st.markdown("### Academic & Clinical References (APA 7th Edition)")
    st.markdown(
        """
        1. **American Diabetes Association**. (2023). Standards of Care in Diabetes—2023. *Diabetes Care*, 46(Suppl. 1), S1–S291. https://doi.org/10.2337/dc23-Sint
        2. **Centers for Disease Control and Prevention**. (2022). *Clinical overview of pneumonia and respiratory syncytial virus*. U.S. Department of Health and Human Services. https://www.cdc.gov/pneumonia/index.html
        3. **Centers for Disease Control and Prevention**. (2023). *Malaria diagnosis and treatment in the United States*. U.S. Department of Health and Human Services. https://www.cdc.gov/malaria/diagnosis_treatment/
        4. **Headache Classification Committee of the International Headache Society (IHS)**. (2018). The International Classification of Headache Disorders, 3rd edition. *Cephalalgia*, 38(1), 1–211. https://doi.org/10.1177/0333102417738202
        5. **National Health Service (NHS)**. (2023). *Health A to Z: Conditions and treatments*. Crown Copyright. https://www.nhs.uk/conditions/
        6. **Russell, S., & Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
        7. **Shortliffe, E. H.** (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.
        8. **World Health Organization**. (2022). *Guidelines for malaria* (WHO Guidelines Approved by the Guidelines Review Committee). World Health Organization. https://www.who.int/publications/i/item/guidelines-for-malaria
        9. **World Health Organization**. (2023). *Dengue guidelines for diagnosis, treatment, prevention and control*. World Health Organization. https://www.who.int/publications/i/item/9789241547871
        10. **Mendeley Data & Kaggle**. (2023). *Disease and Symptoms Dataset 2023*. Mendeley Data, V1. https://data.mendeley.com/datasets/2cxccsxydc/1
        """
    )

    st.markdown("---")

    # Prominent Safety Notice
    st.markdown("### Medical Safety & Ethical Disclaimer")
    st.warning(f"**MANDATORY MEDICAL SAFETY NOTICE:**\n\n{DISCLAIMER_FULL}")
