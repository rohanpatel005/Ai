# Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining

> **Course:** ECSCT24301 – Foundation of AI  
> **Institution:** Adani University, Faculty of Engineering Sciences and Technology (FEST)  
> **Department:** Computer Science and Engineering (AI-ML)  
> **Project Track:** Applied AI Project Track  
> **Academic Year:** 2026  

---

## 1. Project Title
**Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining**  
*Short Application Title:* **Explainable Medical Expert System**

---

## 2. Student Project Team
1. **Jeel Parikh** (USN: `2410111080`) — *Lead: Core AI Reasoning Engines (Forward & Backward Chaining)*
2. **Krish Patel** (USN: `2410111102`) — *Lead: Knowledge Engineering, Validation, & Empirical Benchmarking*
3. **Chintan Patel** (USN: `2410111090`) — *Lead: Data Preprocessing, Kaggle Pipeline, & UI Architecture*

---

## 3. University & Course Information
- **University:** Adani University
- **Faculty:** Faculty of Engineering Sciences and Technology (FEST)
- **Department:** Department of Computer Science and Engineering (AI-ML)
- **Course Code & Title:** ECSCT24301 – Foundation of AI
- **Track:** Applied AI Project Track

---

## 4. Problem Statement
Medical diagnostic decision support systems require rigorous causal auditability, step-by-step transparency, and deterministic safety bounds. Modern deep learning and statistical classifiers function as opaque "black boxes" that correlate symptoms with disease labels without explicit deductive reasoning. When ambiguous, conflicting, or cyclical medical evidence arises, statistical models risk hallucinating diagnoses or silently selecting arbitrary classes. There is an urgent academic and clinical need for transparent, explainable expert systems built upon formal symbolic Artificial Intelligence.

---

## 5. Motivation
In high-stakes clinical and triage education:
1. **Explainability is paramount:** Clinicians and students require formal **WHY** (why a rule fired) and **HOW** (how intermediate deductions chained) justifications.
2. **Deterministic safety:** Symbolic production systems eliminate statistical hallucinations and guarantee reproducible deductions.
3. **Modularity:** Clinical rules can be individually inspected, validated, and updated without requiring expensive model retraining.

---

## 6. Objectives
- Implement classical rule-based AI reasoning from scratch in Python without machine learning or black-box LLM dependencies.
- Implement four distinct reasoning approaches: Simple Symptom Matching (Baseline), Forward Chaining, Backward Chaining, and Prioritized Forward Chaining.
- Build an explicit, verified knowledge base of clinical IF-THEN rules citing WHO, CDC, NHS, and Mayo Clinic guidelines.
- Integrate an automated, secure Kaggle dataset pipeline to benchmark empirical scalability on 4,920 real records.
- Deliver an interactive, modern AI dashboard with Plotly visual analytics, DAG goal-trees, and exportable benchmarks.

---

## 7. Applied AI Project Track Alignment
This project aligns directly with the **Applied AI Track** of Course ECSCT24301. It realizes classical knowledge-based agent design, formal state-space search, deductive inference, cycle-safe recursion, and empirical complexity benchmarking.

---

## 8. Formal PEAS Agent Model
- **Performance Measure (P):** Correct IF-THEN rule premise evaluations; sub-millisecond execution latency; avoidance of false intermediate deductions; complete WHY/HOW causal traces; safe handling of cycles and conflicts.
- **Environment (E):** Symptom-based educational medical reasoning environment consisting of active working memory, authoritative clinical rules, and external benchmark test cases.
- **Actuators (A):** Inferred diagnostic conclusions, interactive Plotly goal trees, chronological reasoning traces, and downloadable CSV/JSON data.
- **Sensors (S):** Selected symptom tokens entered into working memory; target hypothesis queries; benchmark cases.

---

## 9. Environment Characterization
1. **Partially Observable:** The agent senses only the explicitly entered symptoms; occult pathology or lab values remain unobserved.
2. **Deterministic:** Identical symptom facts and rule priorities consistently yield the exact same deductive trajectory.
3. **Sequential:** Intermediate rule firings assert new facts into working memory, directly determining which downstream rules can fire in future iterations.
4. **Static during run:** The knowledge base remains invariant while an inference query is actively executing.
5. **Single-Agent:** Operates autonomously as a symbolic deductive reasoning engine.

---

## 10. Formal State-Space Problem Formulation
- **State ($S$):** Set of propositional facts asserted in working memory: $S = \{f_1, f_2, \dots, f_k\}$.
- **Initial State ($S_0$):** Symptoms provided by the user: $S_0 = \{\text{symptom}_1, \dots, \text{symptom}_m\}$.
- **Action Set ($A$):** `EvaluateRule(R)`, `FireRule(R)`, `AddInferredFact(f)`, `VerifyTarget(G)`, `TerminateInference()`.
- **Successor Function ($T$):** If $\text{Premises}(R) \subseteq S$, then $T(S, \text{FireRule}(R)) = S \cup \{\text{Conclusion}(R)\}$.
- **Goal Test:** Fixpoint reached ($S_{t+1} = S_t$) or target hypothesis $H \in S$.
- **Cost Metrics:** Execution latency (ms), premise evaluations count, rules fired, iterations, and memory usage.

---

## 11. Knowledge Representation Architecture
The knowledge base comprises 39 explicit production rules structured in JSON and CSV:
```json
{
  "rule_id": "R_RESP_01",
  "conditions": ["upper_respiratory_syndrome", "continuous_sneezing", "runny_nose"],
  "conclusion": "common_cold",
  "evidence_weight": 0.88,
  "specificity": 3,
  "priority": 0.75,
  "source": "NHS Health A to Z - Common Cold",
  "source_url": "https://www.nhs.uk/conditions/common-cold/",
  "description": "Upper respiratory syndrome coupled with sneezing and runny nose supports common cold."
}
```
Multi-hop intermediate inference allows syndromic abstractions (e.g. `upper_respiratory_syndrome`) to be deduced and subsequently used to prove terminal etiological diagnoses (`common_cold`).

---

## 12. Implemented AI Reasoning Algorithms
1. **Simple Symptom Matching (Baseline):** Direct condition overlap ratio ($|\text{Premises} \cap S_0| / |\text{Premises}|$). Incapable of multi-hop chaining.
2. **Forward Chaining (Data-Driven):** Starts with known facts; iteratively scans rules and asserts conclusions until fixpoint is reached.
3. **Backward Chaining (Goal-Driven):** Starts from a target hypothesis; recursively resolves required premise conditions using a visited-set cycle guard to prune infinite branches.
4. **Prioritized Forward Chaining:** Optimized forward chaining that dynamically ranks rules before evaluation based on specificity, evidence weight, and working-memory relevance.

---

## 13. Rule Prioritization (Optimization)
Rules are dynamically ranked using the composite score:
$$\text{Priority}(R) = \alpha \times \text{NormSpecificity}(R) + \beta \times \text{EvidenceWeight}(R) + \gamma \times \text{Relevance}(R)$$
*(Defaults: $\alpha = 0.40, \beta = 0.35, \gamma = 0.25$)*  
*Note: Described strictly as domain-specific rule prioritization and inference optimization, not an admissible A* heuristic.*

---

## 14. Theoretical & Empirical Complexity
- **Simple Matching:** $\mathcal{O}(R \times C)$ Time | $\mathcal{O}(R + C)$ Space
- **Forward Chaining:** $\mathcal{O}(I \times R \times C) \le \mathcal{O}(\min(R, F) \times R \times C)$ Time | $\mathcal{O}(F + R)$ Space
- **Backward Chaining:** $\mathcal{O}(B^D)$ worst-case; $\mathcal{O}(R \times C)$ with cycle detection | $\mathcal{O}(D + F)$ Space
- **Prioritized Forward:** $\mathcal{O}(I \times (R \log R + R \times C))$ Time | $\mathcal{O}(F + R)$ Space
- **Empirical Execution Latency:** Sub-millisecond ($0.13$ to $0.30$ ms per query on 39 rules).

---

## 15. Dataset Provenance & Automatic Kaggle Ingestion
- **Configured Dataset:** `itachi9604/disease-symptom-description-dataset`
- **External Mendeley URL:** [Disease and Symptoms Dataset 2023](https://data.mendeley.com/datasets/2cxccsxydc/1)
- **Automatic Downloader (`src/kaggle_downloader.py`):** Automatically detects local copies under `data/raw/dataset.csv`. If absent, securely downloads via official `kagglehub` SDK. Includes offline fallback generator.
- **Security Notice:** Kaggle API credentials (`kaggle.json`) are strictly kept out of Git, source code, and logs via `.gitignore`.

---

## 16. Kaggle Authentication Setup Guide
To configure Kaggle API synchronization on a new machine:
1. Register a free account at [kaggle.com](https://www.kaggle.com).
2. Go to **Account Settings** $\to$ **API** $\to$ click **Create New Token**.
3. Move the downloaded `kaggle.json` into:
   - Windows: `C:\Users\<username>\.kaggle\kaggle.json`
   - Linux / macOS: `~/.kaggle/kaggle.json`
4. The system will now automatically download and update external datasets.

---

## 17. Preprocessing Pipeline & Statistics
Run preprocessing via:
```bash
python scripts/preprocess_dataset.py
```
**Statistical Audit:**
- Raw Records: **4,920**
- Raw Columns: **18**
- Missing Values Handled: **46,992**
- Processed Instances: **4,920**
- Unique Diseases: **41**
- Unique Standardized Symptoms: **131**
- Average Symptoms per Case: **7.45**

---

## 18. End-to-End System Architecture
```
USER INPUTS / BENCHMARK CASE
             ↓
WORKING MEMORY (FACT STATE S_0)
             ↓
AI INFERENCE ENGINE  <--->  EXPLICIT MEDICAL KNOWLEDGE BASE
  ├── Simple Symptom Matching (Baseline)
  ├── Data-Driven Forward Chaining
  ├── Goal-Driven Backward Chaining
  └── Prioritized Forward Chaining
             ↓
CYCLE DETECTION & CONFLICT RESOLUTION
             ↓
EXPLANATION ENGINE (WHY & HOW CAUSAL TRACES)
             ↓
INTERACTIVE STREAMLIT DASHBOARD & PLOTLY VISUALIZATIONS
```

---

## 19. Installation & Setup
```bash
# Clone the repository
git clone https://github.com/adani-university/medical-expert-system.git
cd medical_expert_system

# Install dependencies
pip install -r requirements.txt
```

---

## 20. Running the Application
Launch the interactive AI dashboard:
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 21. Running the Automated Test Suite
Execute the complete automated test suite covering all 20 tests:
```bash
pytest tests/ -v
```
*(All 20 tests pass with 100% success rate).*

---

## 22. Running Benchmarks via CLI
Execute empirical latency and scalability benchmarks:
```bash
python scripts/run_benchmark.py --cases 50
```

---

## 23. Real Empirical Benchmark Results
Empirical evaluation across 25 real benchmark cases on the 39-rule knowledge base:
| Paradigm | Avg Time (ms) | Total Time (ms) | Avg Rules Evaluated | Avg Rules Fired | Iterations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Simple Matching (Baseline)** | 0.199 ms | 4.97 ms | 39.0 | 1.7 | 1.00 |
| **Forward Chaining** | 0.130 ms | 3.26 ms | 45.1 | 0.2 | 1.16 |
| **Backward Chaining** | 0.156 ms | 3.91 ms | 13.4 | 0.2 | 7.60 |
| **Prioritized Forward Chaining** | 0.296 ms | 7.40 ms | 45.1 | 0.2 | 1.16 |

---

## 24. Error & Failure Analysis (14 Scenarios)
All 14 mandatory academic failure-mode scenarios are verified and pass:
1. Empty input $\to$ Safe prompt without crash.
2. Single symptom $\to$ Insufficient premise prompt.
3. Sparse symptoms $\to$ Missing premise explanation.
4. Out-of-vocabulary tokens $\to$ Safely ignored.
5. Irrelevant symptoms $\to$ No spurious cross-syndromic firing.
6. Duplicate symptoms $\to$ Deduplicated by working memory.
7. No matching rule $\to$ Insufficient information status.
8. Multiple rules fired $\to$ Multi-hop sequence recorded.
9. Conflicting hypotheses $\to$ Differential diagnosis table rendered.
10. Cyclic rule loop $\to$ Visited-set cycle guard safely halts recursion.
11. Missing intermediate rule $\to$ Missing premise explained.
12. Scaled knowledge base $\to$ Smooth execution without memory leaks.
13. Deep backward chaining $\to$ Intermediate sub-goals resolved.
14. Unseen custom inputs $\to$ Evaluated dynamically against rules.

---

## 25. Medical Safety & Disclaimer
> **EDUCATIONAL AI PROTOTYPE – NOT A MEDICAL DIAGNOSTIC TOOL**  
> This software is an academic demonstration developed for Course ECSCT24301 (Foundation of AI) at Adani University. It does NOT provide clinical diagnoses, treatments, prescriptions, or emergency triage. Always consult a licensed physician for real healthcare concerns.

---

## 26. Data & Knowledge Downloads
The application provides one-click export buttons for:
- Knowledge Base CSV (`data/knowledge_base/medical_rules.csv`)
- Knowledge Base JSON (`data/knowledge_base/medical_rules.json`)
- Benchmark Summary CSV & JSON (`outputs/benchmark_results/`)
- Chronological Reasoning Traces (CSV)
- Algorithm Comparison Matrix (CSV)

---

## 27. Limitations
- Does not currently incorporate continuous fuzzy premise matching.
- Does not account for patient demographic variables (age, sex, comorbidities).
- Relies on propositional boolean facts rather than full First-Order Predicate Logic.

---

## 28. Future Work
- Extension to Certainty Factors ($CF$) or probabilistic Bayesian networks.
- Implementation of the Rete match algorithm for large-scale production rule execution.
- Integration of laboratory biomarker inputs and longitudinal temporal tracking.

---

## 29. Project Structure
```
medical_expert_system/
├── app.py                      # Central AI Dashboard & routing controller
├── config.py                   # Central configuration & academic metadata
├── requirements.txt            # Python dependencies
├── README.md                   # Complete academic documentation
├── LICENSE                     # MIT License with educational disclaimer
├── .gitignore                  # Security rules excluding credentials & caches
│
├── scripts/
│   ├── download_dataset.py     # CLI dataset downloader
│   ├── preprocess_dataset.py   # CLI preprocessing runner
│   ├── generate_rules.py       # Knowledge base generator
│   └── run_benchmark.py        # CLI benchmark runner
│
├── data/
│   ├── raw/                    # Raw dataset files
│   ├── processed/              # Cleaned tabular dataset
│   ├── benchmark/              # Benchmark test cases JSON
│   └── knowledge_base/         # Verified medical rules (CSV & JSON)
│
├── src/
│   ├── __init__.py
│   ├── models.py               # Data models (Rule, Step, Node, Result)
│   ├── knowledge_base.py       # Knowledge base loader & validator
│   ├── kaggle_downloader.py    # KaggleHub downloader & local cache
│   ├── preprocessing.py        # Token normalizer & case generator
│   ├── data_loader.py          # Data access & caching utilities
│   ├── baseline.py             # Simple Symptom Matcher baseline
│   ├── forward_chaining.py     # Data-driven Forward Chaining engine
│   ├── backward_chaining.py    # Goal-driven Backward Chaining engine
│   ├── prioritized_forward.py  # Prioritized Forward Chaining engine
│   ├── rule_engine.py          # Unified coordinator for all 4 paradigms
│   ├── explanation_engine.py   # Automated WHY and HOW generator
│   ├── conflict_resolution.py  # Differential diagnosis analyzer
│   ├── cycle_detection.py      # Graph-theoretic cycle analysis
│   ├── benchmark.py            # Empirical benchmark engine
│   ├── complexity.py           # Theoretical & empirical scaling
│   ├── evaluation.py           # 14 failure-mode scenario analyzer
│   └── visualization.py        # Plotly performance charts & goal trees
│
├── pages/
│   ├── assessment.py           # Page 2: Symptom Assessment & presets
│   ├── reasoning.py            # Page 3: AI Reasoning & traces
│   ├── backward.py             # Page 4: Backward Chaining explorer
│   ├── comparison.py           # Page 5: Algorithm comparison
│   ├── knowledge_base.py       # Page 6: Knowledge base explorer
│   ├── benchmark.py            # Page 7: Benchmark Lab
│   ├── error_analysis.py       # Page 8: Error analysis
│   ├── methodology.py          # Page 9: Academic methodology
│   ├── dataset.py              # Page 10: Dataset provenance
│   └── about.py                # Page 11: About & references
│
├── tests/
│   ├── test_baseline.py        # Baseline unit tests
│   ├── test_forward.py         # Forward chaining tests
│   ├── test_backward.py        # Backward chaining tests
│   ├── test_priority.py        # Prioritization tests
│   ├── test_cycles.py          # Cycle detection tests
│   ├── test_conflicts.py       # Conflict resolution tests
│   └── test_edge_cases.py      # Edge case & scenario tests
│
├── outputs/
│   ├── charts/                 # Generated chart figures
│   ├── tables/                 # Preprocessing reports & tables
│   └── benchmark_results/      # Saved CSV and JSON benchmark runs
│
└── docs/
    ├── methodology.md          # Formal PEAS & algorithm docs
    ├── complexity.md           # Computational complexity analysis
    ├── ethics.md               # Medical AI ethics & governance
    ├── references.md           # APA 7th edition references
    ├── viva_questions.md       # 13 comprehensive viva questions & answers
    ├── report_outline.md       # Formal PBL report outline
    └── presentation_outline.md # 12-slide presentation outline
```

---

## 30. Verified Academic References
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Shortliffe, E. H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.
- World Health Organization. (2022). *Guidelines for malaria*. WHO Press.
- Centers for Disease Control and Prevention. (2023). *Pneumonia and Respiratory Pathogens*. U.S. DHHS.
