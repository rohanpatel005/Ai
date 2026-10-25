"""
Complexity Analysis Module.
Contains formal theoretical computational complexity formulations and runs empirical
scaling experiments across varying knowledge base sizes and input loads.
"""

from typing import List, Dict, Any, Optional
import pandas as pd

from src.knowledge_base import KnowledgeBase
from src.benchmark import BenchmarkEngine


class ComplexityAnalyzer:
    """
    Evaluates both theoretical and empirical time/space complexity of the reasoning algorithms.
    """

    THEORETICAL_COMPLEXITY = {
        "Simple Matching (Baseline)": {
            "time_complexity": "O(R × C)",
            "space_complexity": "O(R + C)",
            "description": (
                "Performs a single linear pass over all R rules, evaluating C conditions per rule. "
                "No iterations or chaining exist, yielding strictly linear time relative to rule count."
            ),
            "worst_case_trigger": "Large rule base R with high condition count C.",
        },
        "Forward Chaining": {
            "time_complexity": "O(I × R × C) ≤ O(min(R, F) × R × C)",
            "space_complexity": "O(F + R)",
            "description": (
                "Repeats premise evaluations over I iterations until fixpoint. In the worst case, each iteration "
                "infers exactly one fact, bounding I by min(R, F) where F is the maximum fact universe."
            ),
            "worst_case_trigger": "Deep multi-hop chaining cascades where each rule depends sequentially on previous conclusions.",
        },
        "Backward Chaining": {
            "time_complexity": "O(B^D) without memoization; O(R × C) with cycle-visited set",
            "space_complexity": "O(D + F)",
            "description": (
                "Recursively searches sub-goal trees with branching factor B (candidate rules per goal) "
                "up to proof depth D. Visited-path cycle detection prunes infinite branches and guarantees termination."
            ),
            "worst_case_trigger": "High branching factor B combined with deeply nested intermediate goals.",
        },
        "Prioritized Forward Chaining": {
            "time_complexity": "O(I × (R log R + R × C))",
            "space_complexity": "O(F + R)",
            "description": (
                "Calculates dynamic multi-factor priority scores (specificity, evidence, relevance) "
                "and sorts candidate rules prior to each pass. Often reduces practical evaluations through earlier firing."
            ),
            "worst_case_trigger": "Frequent iterations requiring repeated sorting of very large rule queues.",
        },
    }

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        self.kb = knowledge_base if knowledge_base is not None else KnowledgeBase()
        self.benchmarker = BenchmarkEngine(self.kb)

    def run_kb_scaling_experiment(self, kb_sizes: Optional[List[int]] = None, cases_count: int = 15) -> pd.DataFrame:
        """
        Empirically measures execution time and rule evaluation count as KB size increases.
        """
        sizes = kb_sizes or [10, 25, 39, 75, 120]
        scaling_records = []

        for size in sizes:
            res = self.benchmarker.run_benchmark(test_case_count=cases_count, kb_size=size)
            for row in res["summary_rows"]:
                scaling_records.append({
                    "KB_Size": size,
                    "Algorithm": row["Algorithm"],
                    "Avg_Execution_Time_ms": row["Avg Execution Time (ms)"],
                    "Avg_Rules_Evaluated": row["Avg Rules Evaluated"],
                    "Avg_Rules_Fired": row["Avg Rules Fired"],
                    "Avg_Iterations": row["Avg Iterations"],
                })

        return pd.DataFrame(scaling_records)

    def run_case_load_scaling_experiment(self, case_counts: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Empirically measures execution time scaling as the number of input test cases increases.
        """
        counts = case_counts or [5, 15, 30, 50]
        load_records = []

        for count in counts:
            res = self.benchmarker.run_benchmark(test_case_count=count)
            for row in res["summary_rows"]:
                load_records.append({
                    "Test_Cases_Count": count,
                    "Algorithm": row["Algorithm"],
                    "Total_Execution_Time_ms": row["Total Execution Time (ms)"],
                    "Avg_Execution_Time_ms": row["Avg Execution Time (ms)"],
                })

        return pd.DataFrame(load_records)
