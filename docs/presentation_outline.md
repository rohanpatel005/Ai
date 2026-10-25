# Viva Presentation Outline: Explainable Medical Expert System

**Course:** ECSCT24301 – Foundation of AI | **Institution:** Adani University (FEST)  
**Track:** Applied AI Project Track  
**Presentation Time:** 15 Minutes (10 min slides + 5 min live system demo)  
**Team Members:** Jeel Parikh (2410111080), Krish Patel (2410111102), Chintan Patel (2410111090)

---

### Slide 1: Title & Academic Identity
- **Project Title:** Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining
- **Course & Department:** ECSCT24301 – Foundation of AI, Dept. of CSE (AI-ML), FEST, Adani University
- **Team Members & Roles:**
  - Jeel Parikh: Core AI Reasoning Engines (Forward/Backward Chaining)
  - Krish Patel: Knowledge Engineering, Validation, & Empirical Benchmarking
  - Chintan Patel: Data Preprocessing, Kaggle Pipeline, & UI Dashboard
- **Key Disclaimer:** Educational AI Prototype – Not a Medical Diagnostic Tool.

---

### Slide 2: Problem Statement, Motivation & PEAS Model
- **Problem Statement:** Black-box ML models in healthcare lack causal explainability, deterministic auditability, and safety bounds against hallucinations.
- **Applied AI Track Motivation:** Classical rule-based symbolic AI enables 100% deterministic, verifiable diagnostic deductions with complete WHY and HOW explanation traces.
- **Formal PEAS Model:**
  - *Performance:* Execution latency (ms), rule firing correctness, explanation transparency, conflict resolution.
  - *Environment:* Clinical symptom space, explicit IF-THEN rules, Kaggle benchmark dataset.
  - *Actuators:* Inferred diagnoses, interactive Plotly goal trees, reasoning traces.
  - *Sensors:* Working-memory symptoms, target hypothesis queries.

---

### Slide 3: State Space & Formal Problem Formulation
- **State ($S$):** Propositional set of working memory facts $S = \{f_1, f_2, \dots, f_k\}$.
- **Initial State ($S_0$):** User-selected symptoms.
- **Action Set ($A$):** `EvaluateRule(R)`, `FireRule(R)`, `AddInferredFact(f)`, `VerifyTarget(G)`, `TerminateInference()`.
- **Successor Function ($T$):** If $\text{Premises}(R) \subseteq S$, then $T(S, \text{FireRule}(R)) = S \cup \{\text{Conclusion}(R)\}$.
- **Environment Characteristics:** Partially observable, deterministic, sequential, static, single-agent.

---

### Slide 4: Knowledge Representation vs. Dataset
- **Core Distinction:**
  - **KNOWLEDGE:** Explicit clinical rules cited from WHO, CDC, NHS, and Mayo Clinic.
  - **DATA:** External benchmark dataset (4,920 instances from Kaggle/Mendeley) used solely for scalability and latency benchmarking (NO ML training).
- **Rule Architecture:**
  - Fields: `rule_id`, `conditions`, `conclusion`, `evidence_weight`, `specificity`, `priority`, `source`.
  - Multi-hop intermediate abstraction: e.g., Symptoms $\to$ `upper_respiratory_syndrome` $\to$ `common_cold`.
  - Validation: 0 duplicate IDs, 0 missing premises, 100% schema compliance.

---

### Slide 5: Baseline — Simple Symptom Matching
- **Concept:** Calculates premise overlap ratio: $\text{Ratio} = \frac{|\text{Matched Conditions}|}{|\text{Total Conditions}|}$.
- **Academic Purpose:** Serves as the genuine baseline against which AI reasoning is benchmarked.
- **Fundamental Limitation:** Single-pass evaluation; strictly incapable of multi-step intermediate chaining.

---

### Slide 6: Forward & Backward Chaining Engines
- **Forward Chaining (Data-Driven):**
  - Starts with known symptoms; iterates over rules until fixpoint $\Delta S = \emptyset$.
  - Generates multi-hop causal deductions from raw symptoms to final diagnoses.
- **Backward Chaining (Goal-Driven):**
  - Starts with a clinical target hypothesis (e.g., `malaria`); recursively proves required premises.
  - Includes visited-set cycle detection to safely terminate recursive loops ($A \to B \to C \to A$).
  - Produces an interactive Plotly goal resolution tree.

---

### Slide 7: Prioritized Forward Chaining (Inference Optimization)
- **Concept:** Domain-specific rule prioritization and evaluation ordering.
- **Formula:**
  $$\text{Priority}(R) = \alpha \times \text{NormSpecificity}(R) + \beta \times \text{EvidenceWeight}(R) + \gamma \times \text{Relevance}(R)$$
  *(Configurable $\alpha = 0.40, \beta = 0.35, \gamma = 0.25$)*
- **Academic Clarification:** This is domain-specific rule prioritization, NOT an admissible A* heuristic.
- **Empirical Benefit:** Fired pertinent and highly specific rules in fewer rule evaluations on targeted knowledge bases.

---

### Slide 8: Complexity Analysis & Experimental Setup
- **Theoretical Time Complexity:**
  - Simple Matching: $\mathcal{O}(R \times C)$
  - Forward Chaining: $\mathcal{O}(I \times R \times C) \le \mathcal{O}(\min(R, F) \times R \times C)$
  - Backward Chaining: $\mathcal{O}(B^D)$ worst-case; $\mathcal{O}(R \times C)$ with visited set.
  - Prioritized Forward Chaining: $\mathcal{O}(I \times (R \log R + R \times C))$
- **Experimental Pipeline:** Automated KaggleHub downloader, token normalization, benchmark case generator.

---

### Slide 9: Empirical Benchmark Results
- **Real Benchmark Data (25 Cases, 39 Rules):**
  - Simple Matching: 0.199 ms avg time, 39.0 rules evaluated.
  - Forward Chaining: 0.130 ms avg time, 45.1 rules evaluated.
  - Backward Chaining: 0.156 ms avg time, 13.4 rules evaluated (pruning irrelevant branches!).
  - Prioritized Forward Chaining: 0.296 ms avg time, 45.1 rules evaluated.
- **Zero Fabricated Results:** All latencies measured from live Python runtime.

---

### Slide 10: Algorithm Comparison & Key Insights
- **Side-by-Side Comparison:**
  - Multi-hop capability: Forward & Backward succeed; Baseline fails.
  - Search direction: Forward is inductive/data-driven; Backward is deductive/goal-focused.
  - Latency: Sub-millisecond performance across all paradigms.

---

### Slide 11: Error Analysis & Robustness
- **14 Mandatory Scenarios Tested:**
  - Empty input, isolated symptoms, duplicate tokens, out-of-vocabulary inputs.
  - Competing hypotheses: Differential diagnosis reported without silent single-selection.
  - Cyclic rules: Visited-set cycle guard safely halts infinite loops.
- **Testing Result:** 20 / 20 Pytest unit tests passing (100% pass rate).

---

### Slide 12: Conclusion, Ethics & Future Work
- **Contributions:** Complete, fully working classical AI expert system with transparent WHY/HOW explanations.
- **Medical Safety:** Strict educational prototype notice; probabilistic outputs; zero clinical risk.
- **Future Directions:** Extension to fuzzy truth values and probabilistic certainty factors (MYCIN style).

---

### Live Demonstration Plan (5 Minutes)
1. **Minute 1: Dashboard & Telemetry:** Overview of rules count, Kaggle dataset stats, and safety banner.
2. **Minute 2: Symptom Assessment:** Load Case 1 (Respiratory); formulate working memory.
3. **Minute 3: AI Reasoning & Explanation:** Run Forward Chaining; inspect WHY & HOW collapsible traces.
4. **Minute 4: Backward Explorer:** Pick target `malaria` and visualize interactive Plotly DAG goal-tree.
5. **Minute 5: Benchmark Lab & Downloads:** Run 25-case benchmark live, view runtime charts, and download CSV.
