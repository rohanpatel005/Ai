"""
Page 9: Academic Methodology & Foundation of AI Documentation.
Details Problem Formulation, PEAS Model, Environment Characterization, State Space,
Algorithms, Complexity Analysis, and Classical AI Principles.
"""

import streamlit as st
import pandas as pd

from config import (
    DISCLAIMER_SHORT,
    UNIVERSITY_NAME,
    FACULTY_NAME,
    DEPARTMENT_NAME,
    COURSE_CODE,
    COURSE_NAME,
    PROJECT_TRACK,
    PROJECT_TITLE,
)
from src.complexity import ComplexityAnalyzer
from src.visualization import Visualizer


def render_methodology_page():
    st.markdown("## Academic Methodology & AI Formulation")
    st.caption(f"{UNIVERSITY_NAME} | {FACULTY_NAME} | {COURSE_CODE} - {COURSE_NAME}")

    tab_peas, tab_state, tab_algos, tab_complexity = st.tabs([
        "1. PEAS & Environment",
        "2. State & Problem Formulation",
        "3. Algorithms & Optimization",
        "4. Complexity Analysis & Scalability",
    ])

    with tab_peas:
        st.markdown("### Formal PEAS Agent Formulation")
        st.write(
            "In classical Artificial Intelligence (Russell & Norvig, 2020), an intelligent agent is specified by its "
            "**Performance Measure, Environment, Actuators, and Sensors (PEAS)**:"
        )

        st.markdown(
            """
            | Component | Specification for Medical Expert System |
            | :--- | :--- |
            | **Performance Measure (P)** | • Correct and valid IF-THEN rule firings without false intermediate inferences.<br>• Inference execution time (sub-millisecond latency).<br>• Premise evaluation efficiency (minimizing redundant rule checks).<br>• High explanation transparency (traceability of WHY and HOW).<br>• Safe and unambiguous handling of differential conflicts and circular loops. |
            | **Environment (E)** | • Symptom-based educational medical reasoning environment.<br>• Explicit knowledge base of medical rules derived from WHO, CDC, NHS, and Mayo Clinic.<br>• External benchmark cases sourced from Kaggle and clinical repositories.<br>• Active user working memory. |
            | **Actuators (A)** | • Display inferred diagnostic hypotheses and intermediate syndromic facts.<br>• Render interactive recursive goal-trees (Backward Chaining).<br>• Output chronologically indexed execution traces and WHY/HOW explanations.<br>• Emit medical safety notices and conflict warnings.<br>• Export structured CSV and JSON benchmark results. |
            | **Sensors (S)** | • User-selected symptom tokens entered into working memory.<br>• User-selected target hypothesis for backward query proving.<br>• External benchmark instances loaded during empirical evaluation.<br>• Rule constraints and weights loaded from the knowledge base. |
            """
        )

        st.markdown("### Environment Characterization")
        st.markdown(
            """
            The environment in which this symbolic reasoning agent operates exhibits five primary properties:

            1. **Partially Observable**: The agent only senses the explicitly reported symptom subset. Subclinical, asymptomatic, or lab-test variables remain unobserved.
            2. **Deterministic**: Given an identical set of initial symptom facts and an identical rule priority ordering, rule evaluation and firing produce deterministic, reproducible deduction trajectories.
            3. **Sequential**: Current rule firings alter working memory by asserting new intermediate facts (e.g., `upper_respiratory_syndrome`), which directly determine which subsequent rules are satisfied in future passes.
            4. **Static during Run**: The knowledge base remains fixed throughout an inference session; the world does not dynamically shift while the rule engine executes.
            5. **Single-Agent Symbolic Reasoning**: The agent reasons autonomously without adversarial or cooperative multi-agent dynamics.
            """
        )

    with tab_state:
        st.markdown("### Formal Search & State Space Formulation")
        st.markdown(
            """
            - **State Representation ($S$)**: A symbolic state is represented as a set or boolean dictionary of currently known facts:
              $$S = \\{ f_1, f_2, \\dots, f_k \\}$$
            - **Initial State ($S_0$)**: The set of symptom tokens entered by the user:
              $$S_0 = \\{ \\text{symptom}_1, \\text{symptom}_2, \\dots, \\text{symptom}_m \\}$$
            - **Action Set ($A$)**:
              1. `EvaluateRule(R_i)`: Match premise conditions $\\text{Premise}(R_i) \\subseteq S$.
              2. `FireRule(R_i)`: Assert conclusion $\\text{Conclusion}(R_i)$ into working memory.
              3. `AddInferredFact(f)`: Update $S \\leftarrow S \\cup \\{f\\}$.
              4. `VerifyTarget(G)`: In backward chaining, test if goal $G \\in S$.
              5. `TerminateInference()`: Stop when fixpoint $\\Delta S = \\emptyset$ is reached or target is proved.
            - **Successor Function ($T$)**:
              Applying a satisfied rule $R$ transforms state $S$ into:
              $$S' = S \\cup \\{ \\text{Conclusion}(R) \\}$$
            - **Goal Test**:
              - *Forward Chaining*: System reaches fixpoint ($S_{t+1} = S_t$) or derives target hypothesis $H \\in S$.
              - *Backward Chaining*: Recursive proof tree establishes $H$ from $S_0$.
            - **Cost Metrics**:
              Measured empirically: execution time in milliseconds, rules evaluated, rules fired, iteration count, and memory footprint.
            """
        )

    with tab_algos:
        st.markdown("### Core Reasoning Paradigms")
        st.markdown(
            """
            #### 1. Simple Symptom Matching (Baseline)
            - **Principle**: Direct matching score $\\text{Score}(R) = \\frac{|\\text{Premises}(R) \\cap S_0|}{|\\text{Premises}(R)|}$.
            - **Limitation**: Evaluates single-level overlap; strictly incapable of multi-hop intermediate inference.

            #### 2. Forward Chaining (Data-Driven Reasoning)
            - **Principle**: Starts from initial symptoms, evaluates all rule premises, fires satisfied rules, asserts new facts into memory, and iterates until no new facts can be deduced (fixpoint).
            - **Capability**: Enables multi-hop abstraction: e.g., symptoms $\\to$ intermediate syndrome $\\to$ terminal disease.

            #### 3. Backward Chaining (Goal-Driven Reasoning)
            - **Principle**: Starts from a chosen clinical target hypothesis, queries rules concluding that target, and recursively seeks to establish premise conditions against known facts or sub-goals.
            - **Cycle Guard**: Maintains a recursion `visited_set` to detect cyclic definitions ($A \\to B \\to C \\to A$) and prevent infinite call stacks.

            #### 4. Prioritized Forward Chaining (Inference Optimization)
            - **Formula**:
              $$\\text{Priority}(R) = \\alpha \\times \\text{NormSpecificity}(R) + \\beta \\times \\text{EvidenceWeight}(R) + \\gamma \\times \\text{Relevance}(R)$$
            - **Academic Designation**: Termed *domain-specific rule prioritization and inference optimization* (NOT an admissible A* heuristic).
            - **Benefit**: Reorders rule evaluation queue so that highly specific, medically grounded, and relevant rules fire first.
            """
        )

    with tab_complexity:
        st.markdown("### Complexity Analysis (Theoretical & Empirical)")

        st.markdown("#### Theoretical Complexity Bounds")
        comp_data = []
        for name, data in ComplexityAnalyzer.THEORETICAL_COMPLEXITY.items():
            comp_data.append({
                "Algorithm": name,
                "Time Complexity": data["time_complexity"],
                "Space Complexity": data["space_complexity"],
                "Description": data["description"],
            })
        st.table(comp_data)

        st.markdown("#### Empirical Scalability Curves")
        st.write("Generate live empirical complexity scaling curves across knowledge base sizes and test case loads:")

        if st.button("Generate Live Empirical Complexity Graphs"):
            with st.spinner("Executing scalability benchmark runs..."):
                analyzer = ComplexityAnalyzer()
                df_kb_scaling = analyzer.run_kb_scaling_experiment(kb_sizes=[10, 25, 39, 75, 120], cases_count=10)
                df_load_scaling = analyzer.run_case_load_scaling_experiment(case_counts=[5, 15, 30, 50])

                st.session_state["complexity_kb_df"] = df_kb_scaling
                st.session_state["complexity_load_df"] = df_load_scaling

        if "complexity_kb_df" in st.session_state:
            fig_kb = Visualizer.plot_kb_scaling(st.session_state["complexity_kb_df"])
            st.plotly_chart(fig_kb, use_container_width=True)

            fig_load = Visualizer.plot_load_scaling(st.session_state["complexity_load_df"])
            st.plotly_chart(fig_load, use_container_width=True)
        else:
            st.info("Click the button above to execute live scaling experiments and generate empirical complexity curves.")
