# Comprehensive Methodology & Formal AI Documentation

**Course:** ECSCT24301 – Foundation of AI  
**Track:** Applied AI Project Track  
**Institution:** Adani University, Faculty of Engineering Sciences and Technology (FEST)  
**Project:** Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining  

---

## 1. Problem Definition & Academic Track
The objective of this project is to develop an educational, explainable, and fully functional Medical Expert System utilizing classical symbolic Artificial Intelligence. In modern medical informatics, clinical triage and differential diagnosis require 100% auditable and causal reasoning traces. While statistical machine learning models achieve high accuracy on benchmark datasets, their lack of explicit logic mechanisms ("black-box problem") poses significant barriers to trust, accountability, and clinical explainability.

As part of the **Applied AI Project Track**, this project implements classical symbolic deduction engines from first principles in Python—including Forward Chaining, Backward Chaining, and Rule Prioritization—operating on an explicit knowledge base of clinical rules cited from authoritative public health organizations (WHO, CDC, NHS, Mayo Clinic).

---

## 2. Formal PEAS Agent Specification

| PEAS Component | Implementation in Medical Expert System |
| :--- | :--- |
| **Performance Measure (P)** | • Correctness of IF-THEN premise evaluations without spurious deductions.<br>• Computational latency in milliseconds (sub-millisecond target).<br>• Branching factor and search tree efficiency in backward goal resolution.<br>• Transparency and completeness of causal WHY and HOW explanation traces.<br>• Safe handling of cyclical rule definitions and multi-hypothesis conflicts. |
| **Environment (E)** | • Symptom-based educational medical reasoning environment.<br>• Working memory containing current factual assertions.<br>• Explicit knowledge base of 39 verified clinical production rules.<br>• Benchmark test cases derived from Kaggle and Mendeley data. |
| **Actuators (A)** | • Display inferred diagnostic hypotheses and intermediate syndromic facts.<br>• Render interactive Plotly goal-trees and execution timelines.<br>• Present structured WHY and HOW explanation narratives.<br>• Emit medical safety notices and conflict warnings.<br>• Export real-time CSV and JSON performance benchmarks. |
| **Sensors (S)** | • User-selected symptom tokens entered via the interactive UI.<br>• Target hypothesis queries submitted for backward chaining proof.<br>• Benchmark test cases loaded during scalability testing.<br>• Knowledge base rules and evidence weights. |

---

## 3. Environment Characterization

1. **Partially Observable**: The system only senses symptoms that are explicitly provided in working memory. Sub-clinical physiological parameters, occult pathology, and laboratory biomarkers remain unobserved.
2. **Deterministic**: Given a specific set of initial symptom facts and fixed rule priorities, the inference engine produces identical, reproducible reasoning chains every time.
3. **Sequential**: Each rule firing asserts a new fact into working memory (e.g., `upper_respiratory_syndrome`), altering the state and directly determining which subsequent rules can fire in subsequent passes.
4. **Static**: The knowledge base rules and parameters do not change dynamically while an inference query is executing.
5. **Single-Agent**: The reasoning engine operates as an autonomous symbolic agent without competitive or cooperative multi-agent interactions.

---

## 4. State-Space Problem Formulation

- **State Representation ($S$)**: A symbolic state is represented as a set of propositional facts currently asserted in working memory:
  $$S = \{ f_1, f_2, \dots, f_k \}$$
- **Initial State ($S_0$)**: The initial set of symptoms provided by the user:
  $$S_0 = \{ \text{symptom}_1, \text{symptom}_2, \dots, \text{symptom}_m \}$$
- **Action Set ($A$)**:
  1. $\text{EvaluateRule}(R)$: Check whether all premise conditions of rule $R$ are satisfied in $S$.
  2. $\text{FireRule}(R)$: Deduce the rule conclusion and record the firing in the execution trace.
  3. $\text{AddInferredFact}(f)$: Update the working memory state: $S \leftarrow S \cup \{f\}$.
  4. $\text{VerifyTarget}(G)$: In backward chaining, check if sub-goal $G \in S$.
  5. $\text{TerminateInference}()$: Conclude reasoning when fixpoint $\Delta S = \emptyset$ is reached or target goal is proved.
- **Successor Function ($T$)**:
  Applying a satisfied rule $R$ with premise $\text{Premises}(R) \subseteq S$ yields:
  $$T(S, \text{FireRule}(R)) = S \cup \{ \text{Conclusion}(R) \}$$
- **Goal Test**:
  - *Forward Chaining*: System reaches fixpoint ($S_{t+1} = S_t$) or establishes target hypothesis $H \in S$.
  - *Backward Chaining*: Recursive proof tree establishes that target $H$ logically follows from $S_0$.
- **Cost Metrics**:
  Execution time (ms), rules evaluated count, rules fired count, inference iterations count, and memory consumption.

---

## 5. Knowledge Representation & Multi-Hop Chaining
The knowledge base comprises 39 production rules structured as:
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

### Multi-Hop Intermediate Inference Architecture
To demonstrate true classical AI reasoning beyond simple keyword matching, rules are organized into hierarchical abstraction tiers:
1. **Tier 1 (Syndromic Abstraction)**: Groups raw symptoms into clinical syndromes:
   $$\text{fever} \land \text{cough} \land \text{sore\_throat} \implies \text{upper\_respiratory\_syndrome}$$
2. **Tier 2 (Specific Etiological Diagnosis)**: Combines intermediate syndromes with specific clinical markers:
   $$\text{upper\_respiratory\_syndrome} \land \text{continuous\_sneezing} \land \text{runny\_nose} \implies \text{common\_cold}$$

---

## 6. Algorithmic Formulations

### Algorithm 1: Simple Symptom Matching (Baseline)
Calculates raw premise overlap without chaining:
$$\text{Score}(R) = \frac{|\text{Premises}(R) \cap S_0|}{|\text{Premises}(R)|}$$
Fires if $\text{Score}(R) \ge \theta$. Incapable of multi-hop deductions.

### Algorithm 2: Forward Chaining (Data-Driven Reasoning)
```text
FUNCTION ForwardChaining(initial_facts, rules):
    known_facts = copy(initial_facts)
    fired_rules = []
    iterations = 0
    LOOP:
        iterations += 1
        changes = False
        FOR EACH rule IN rules:
            IF rule not already fired AND Premises(rule) subset of known_facts:
                IF Conclusion(rule) not in known_facts:
                    known_facts.add(Conclusion(rule))
                    fired_rules.append(rule)
                    changes = True
        IF NOT changes OR iterations >= MAX_LIMIT:
            BREAK
    RETURN known_facts, fired_rules, iterations
```

### Algorithm 3: Backward Chaining (Goal-Driven Reasoning)
```text
FUNCTION ProveGoal(goal, known_facts, visited_path, depth):
    IF goal in known_facts:
        RETURN True, Node(goal, PROVEN_FACT)
    IF goal in visited_path:
        RETURN False, Node(goal, CYCLE_DETECTED)
    IF depth > MAX_DEPTH:
        RETURN False, Node(goal, FAILED)
    
    visited_path.add(goal)
    candidate_rules = FindRulesConcluding(goal)
    FOR EACH rule IN candidate_rules:
        all_proven = True
        FOR EACH premise IN Premises(rule):
            success, child = ProveGoal(premise, known_facts, visited_path, depth + 1)
            IF NOT success:
                all_proven = False
                BREAK
        IF all_proven:
            known_facts.add(goal)
            visited_path.remove(goal)
            RETURN True, Node(goal, PROVEN_RULE)
    visited_path.remove(goal)
    RETURN False, Node(goal, FAILED)
```

### Algorithm 4: Prioritized Forward Chaining
At each pass, eligible rules are ranked by:
$$\text{Priority}(R) = \alpha \times \frac{\text{Specificity}(R)}{\text{MaxSpec}} + \beta \times \text{Weight}(R) + \gamma \times \frac{|\text{Premises}(R) \cap S|}{|\text{Premises}(R)|}$$
Defaults: $\alpha = 0.40, \beta = 0.35, \gamma = 0.25$. Evaluates and fires highest priority rules first.
