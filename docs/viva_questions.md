# Viva Voce Examination Guide: Questions & Model Answers

**Course:** ECSCT24301 – Foundation of AI  
**Track:** Applied AI Project Track  
**Project:** Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining  
**Institution:** Adani University, Faculty of Engineering Sciences and Technology (FEST)  
**Department:** Computer Science and Engineering (AI-ML)  
**Team Members:**
1. Jeel Parikh (USN: 2410111080)
2. Krish Patel (USN: 2410111102)
3. Chintan Patel (USN: 2410111090)

---

### Q1. What is an Intelligent Agent, and how is it realized in this project?
**Answer:** An intelligent agent is an entity that perceives its environment through sensors and acts upon that environment through actuators to achieve specified goals (Russell & Norvig, 2020). In this project, the agent perceives symptom inputs and target queries, maintains an internal state (working memory), reasons over an explicit knowledge base using formal inference mechanisms, and acts by asserting new facts, detecting conflicts/cycles, and displaying explanatory deductions.

---

### Q2. Explain the formal PEAS model for your system.
**Answer:**
- **Performance Measure (P):** Correct premise matching; sub-millisecond execution latency; avoidance of false intermediate deductions; transparency of WHY and HOW explanations; safe handling of cycles and conflicts.
- **Environment (E):** Symptom-based educational medical reasoning environment consisting of active working memory, authoritative clinical IF-THEN rules, and Kaggle/Mendeley benchmark test instances.
- **Actuators (A):** User interface displays presenting inferred diagnoses, interactive Plotly goal trees, chronological reasoning traces, and downloadable CSV/JSON artifacts.
- **Sensors (S):** Selected symptom tokens entered by the user or loaded from benchmark cases; target goal inputs.

---

### Q3. How do you characterize the environment?
**Answer:**
1. **Partially Observable:** The agent only perceives explicitly entered symptoms; latent subclinical biomarkers or lab tests are unobserved.
2. **Deterministic:** Identical symptom inputs and rule priorities always yield the exact same deductive trajectory.
3. **Sequential:** An action (firing a rule) asserts a new fact (e.g., `upper_respiratory_syndrome`), which directly enables downstream rules to fire in subsequent iterations.
4. **Static during run:** The knowledge base remains invariant while the inference engine evaluates a query.
5. **Single-Agent:** Reasoning is carried out independently by a symbolic inference engine without competing or cooperating agents.

---

### Q4. What is the formal State Space formulation of your system?
**Answer:**
- **State ($S$):** A set of propositional facts currently known to be true in working memory: $S = \{f_1, f_2, \dots, f_k\}$.
- **Initial State ($S_0$):** The set of symptoms entered by the user: $S_0 = \{\text{symptom}_1, \dots, \text{symptom}_m\}$.
- **Action Set ($A$):** `EvaluateRule(R)`, `FireRule(R)`, `AddInferredFact(f)`, `VerifyTarget(G)`, `TerminateInference()`.
- **Successor Function ($T$):** If premise conditions $\text{Premises}(R) \subseteq S$, then $T(S, \text{FireRule}(R)) = S \cup \{\text{Conclusion}(R)\}$.
- **Goal Test:** Fixpoint reached ($S_{t+1} = S_t$) or target hypothesis $H \in S$.
- **Cost Metrics:** Execution latency (ms), premise evaluations count, rules fired count, iteration passes, and memory footprint.

---

### Q5. What is the difference between Data and Knowledge in this project?
**Answer:**
- **DATA (= Benchmark Instances):** External dataset cases (e.g. from Kaggle/Mendeley) containing symptom vectors used strictly to test, evaluate, and benchmark algorithmic scalability. No ML training is performed.
- **KNOWLEDGE (= Explicit Rules):** Authoritative, modular IF-THEN rules sourced and cited from published clinical guidelines (WHO, CDC, NHS, Mayo Clinic).
- **REASONING (= Classical AI):** Logical evaluation of data against knowledge via Forward, Backward, and Prioritized chaining.

---

### Q6. Why use Classical Rule-Based AI instead of Machine Learning or LLMs?
**Answer:**
1. **Total Explainability:** In high-stakes medical and diagnostic education, black-box statistical classifiers cannot guarantee step-by-step causal transparency. Our expert system provides 100% deterministic WHY and HOW traces.
2. **No Data Hallucinations:** LLMs frequently hallucinate plausible-sounding but erroneous medical facts. A rule-based production system fires strictly when explicit premises are formally verified.
3. **Auditability and Knowledge Modification:** Adding or revising a medical guideline only requires editing a specific declarative rule without requiring expensive retraining or risking catastrophic forgetting.

---

### Q7. How does Forward Chaining work in your implementation?
**Answer:** Forward Chaining is a **data-driven (bottom-up)** algorithm. It begins with the initial facts in working memory. In each iteration, it scans all rules in the knowledge base. For any rule whose premise conditions are entirely present in working memory and whose conclusion has not yet been added, it fires the rule and asserts the conclusion into memory. This repeats until a fixpoint is established (no new facts added) or a target is reached.

---

### Q8. How does Backward Chaining work, and how do you handle circular loops?
**Answer:** Backward Chaining is a **goal-driven (top-down)** algorithm. It begins with a target hypothesis $G$. It locates rules concluding $G$ and recursively attempts to prove their premise conditions. If a condition is already in working memory, it succeeds (`PROVEN_FACT`). If not, it treats that condition as a sub-goal and recurses.
To prevent infinite loops from circular definitions (e.g., $A \to B \to C \to A$), we maintain a `visited_path` set. If a sub-goal is encountered that is already on the current proof branch, the engine halts that branch immediately, marks `CYCLE_DETECTED`, and safely prunes the recursion without crashing.

---

### Q9. What is your Baseline, and why is it simpler than the AI algorithms?
**Answer:** Our baseline is **Simple Symptom Matching**. It calculates the direct ratio:
$$\text{Score}(R) = \frac{|\text{Premises}(R) \cap S_0|}{|\text{Premises}(R)|}$$
It is fundamentally simpler because it performs a single pass over rules and **cannot perform multi-hop chaining**. For instance, it cannot deduce an intermediate syndrome (e.g., `upper_respiratory_syndrome`) and use that to subsequently prove `common_cold`.

---

### Q10. What is Prioritized Forward Chaining, and why is it NOT an admissible heuristic?
**Answer:** Prioritized Forward Chaining is an optimization technique where candidate rules are ordered before evaluation using a composite priority score:
$$\text{Priority}(R) = \alpha \times \text{NormSpecificity}(R) + \beta \times \text{EvidenceWeight}(R) + \gamma \times \text{Relevance}(R)$$
It is strictly described as **domain-specific rule prioritization and inference optimization**. We do NOT call it an "admissible heuristic" because an admissible heuristic in A* search mathematically must never overestimate the cost to reach a goal. In rule-based expert systems, rule prioritization re-ranks evaluation queues to prioritize highly specific and pertinent rules first, which has no mathematical isomorphism to admissible graph heuristics.

---

### Q11. How do you handle Conflict Resolution when multiple diagnoses fire?
**Answer:** When symptoms satisfy premises for multiple diseases simultaneously (e.g., viral fever vs acute fatigue), our system **strictly avoids silently picking one hypothesis**. The `ConflictResolver` compiles a structured differential diagnosis table presenting all supported hypotheses, their supporting rule IDs, matched premises, evidence weights, and authoritative clinical citations.

---

### Q12. What are the theoretical and empirical time complexities?
**Answer:**
- **Simple Matching:** $\mathcal{O}(R \times C)$ linear in rules and conditions.
- **Forward Chaining:** $\mathcal{O}(I \times R \times C) \le \mathcal{O}(\min(R, F) \times R \times C)$ where $I$ is iterations and $F$ is facts.
- **Backward Chaining:** $\mathcal{O}(B^D)$ worst-case tree search without memoization; bounded to $\mathcal{O}(R \times C)$ with visited-set cycle detection.
- **Prioritized Forward Chaining:** $\mathcal{O}(I \times (R \log R + R \times C))$ due to dynamic queue sorting per pass.
Empirical benchmark results demonstrate sub-millisecond execution (0.1 to 0.7 ms per case on 39 rules).

---

### Q13. What is the Medical Safety policy of your system?
**Answer:** This software is strictly an **educational AI prototype** for course ECSCT24301. It displays prominent disclaimers on every page, does NOT provide prescriptions, clinical certainties, or emergency medical instructions, and qualifies all outputs probabilistically or evidentially ("Based on the selected symptoms and the implemented knowledge rules, the system inferred...").
