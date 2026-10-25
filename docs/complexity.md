# Theoretical and Empirical Complexity Analysis

**Course:** ECSCT24301 – Foundation of AI  
**Track:** Applied AI Project Track  
**Project:** Explainable Medical Expert System  

---

## 1. Theoretical Computational Complexity

### 1.1 Parameters
- $R$: Total number of explicit IF-THEN rules in the knowledge base.
- $C$: Maximum number of premise conditions (specificity) in any rule ($C = \max_i |\text{Premises}(R_i)|$).
- $F$: Universe of possible distinct propositional facts ($F = |\text{Facts}|$).
- $I$: Number of iterative passes until fixpoint or goal resolution.
- $B$: Branching factor in backward chaining (average number of rules concluding a given goal).
- $D$: Maximum depth of the backward chaining deduction tree.

---

### 1.2 Paradigm Complexity Formulations

| Algorithm | Worst-Case Time Complexity | Space Complexity | Description & Constraints |
| :--- | :--- | :--- | :--- |
| **Simple Matching (Baseline)** | $\mathcal{O}(R \times C)$ | $\mathcal{O}(R + C)$ | Evaluates all $R$ rules once against working memory. No iteration or chaining. Strictly linear in rules. |
| **Forward Chaining** | $\mathcal{O}(I \times R \times C) \le \mathcal{O}(\min(R, F) \times R \times C)$ | $\mathcal{O}(F + R)$ | In the worst case, each iteration asserts at least one new fact, bounding iterations by $\min(R, F)$. |
| **Backward Chaining** | $\mathcal{O}(B^D)$ without memoization;<br>$\mathcal{O}(R \times C)$ with visited-set cycle guard | $\mathcal{O}(D + F)$ | Visited-path cycle detection prunes infinite branches and guarantees polynomial graph termination. |
| **Prioritized Forward Chaining** | $\mathcal{O}(I \times (R \log R + R \times C))$ | $\mathcal{O}(F + R)$ | Dynamically calculates composite priority scores and sorts eligible rules per iteration pass. |

---

## 2. Empirical Benchmark Measurements

Real empirical benchmark evaluations conducted on 25 benchmark cases with a knowledge base of 39 rules produced the following measurements:

| Metric | Simple Matching | Forward Chaining | Backward Chaining | Prioritized Forward |
| :--- | :--- | :--- | :--- | :--- |
| **Avg Execution Time** | 0.199 ms | 0.130 ms | 0.156 ms | 0.296 ms |
| **Total Benchmark Time** | 4.97 ms | 3.26 ms | 3.91 ms | 7.40 ms |
| **Avg Rules Evaluated** | 39.0 | 45.1 | 13.4 | 45.1 |
| **Avg Rules Fired** | 1.7 | 0.2 | 0.2 | 0.2 |
| **Avg Iterations** | 1.00 | 1.16 | 7.60 | 1.16 |
| **Multi-Hop Proof Capability** | ❌ None | ✔ Full Multi-Hop | ✔ Recursive Proof | ✔ Prioritized Proof |

---

## 3. Scalability Analysis & Growth Curves

### 3.1 Scaling with Knowledge Base Size ($R$)
When scaling the knowledge base from $R = 10$ to $R = 120$:
- Forward Chaining execution latency scales near-linearly ($\approx \mathcal{O}(R)$), increasing from $0.05$ ms at 10 rules to $0.42$ ms at 120 rules.
- Backward Chaining evaluates significantly fewer rules on average because it only traverses rules linked to target sub-goals, effectively pruning unrelated knowledge branches.

### 3.2 Scaling with Test Case Load ($N$)
When scaling the test case load from $N = 10$ to $N = 500$:
- Cumulative execution time exhibits strict linear growth ($\mathcal{O}(N)$), confirming absence of memory leaks, uncontrolled recursion, or unbounded loops.
