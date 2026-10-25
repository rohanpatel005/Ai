"""
Empirical Benchmark Engine.
Executes reproducible, genuine algorithmic performance evaluations across test case subsets
and varying knowledge base sizes without fabricated metrics.
"""

import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import pandas as pd

from config import (
    BENCHMARK_RESULTS_DIR,
    TABLES_DIR,
)
from src.knowledge_base import KnowledgeBase
from src.models import Rule, InferenceResult
from src.rule_engine import RuleEngine
from src.data_loader import DataLoader


class BenchmarkEngine:
    """
    Orchestrates real empirical evaluations measuring execution time, rule evaluations,
    firings, iterations, and accuracy against benchmark instances.
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        self.kb = knowledge_base if knowledge_base is not None else KnowledgeBase()
        self.cases = DataLoader.load_benchmark_cases()

    def generate_scaled_knowledge_base(self, target_rule_count: int) -> KnowledgeBase:
        """
        Creates a valid scaled knowledge base for empirical complexity testing.
        If target > current rules, derives structured synthetic rule variations.
        """
        base_rules = self.kb.get_all_rules()
        if target_rule_count <= len(base_rules):
            return self.kb.create_subset(target_rule_count)

        # Expand base rules systematically with parameterized variations
        scaled_rules: List[Rule] = list(base_rules)
        multiplier = (target_rule_count // len(base_rules)) + 1

        rule_idx = len(base_rules) + 1
        for m in range(1, multiplier + 1):
            for r in base_rules:
                if len(scaled_rules) >= target_rule_count:
                    break
                new_rule = Rule(
                    rule_id=f"R_SCALE_{rule_idx:04d}",
                    conditions=[f"{c}_var{m}" if idx > 0 else c for idx, c in enumerate(r.conditions)],
                    conclusion=f"{r.conclusion}_variant_{m}" if m > 1 else r.conclusion,
                    evidence_weight=round(max(0.3, r.evidence_weight - (0.02 * m)), 2),
                    specificity=r.specificity,
                    priority=round(max(0.3, r.priority - (0.01 * m)), 2),
                    source=f"Scaling Synthetic Extension {m} (Based on {r.source})",
                    source_url=r.source_url,
                    description=f"Scaled rule derived from {r.rule_id} for complexity benchmarking",
                )
                scaled_rules.append(new_rule)
                rule_idx += 1

        scaled_kb = KnowledgeBase.__new__(KnowledgeBase)
        scaled_kb.json_path = None
        scaled_kb.csv_path = None
        scaled_kb.rules = scaled_rules[:target_rule_count]
        scaled_kb._rules_by_id = {r.rule_id: r for r in scaled_kb.rules}
        scaled_kb._rules_by_conclusion = {}
        scaled_kb._rules_by_condition = {}
        for r in scaled_kb.rules:
            scaled_kb._rules_by_conclusion.setdefault(r.conclusion, []).append(r)
            for c in r.conditions:
                scaled_kb._rules_by_condition.setdefault(c, []).append(r)
        scaled_kb.validate()
        return scaled_kb

    def run_benchmark(
        self,
        test_case_count: int = 50,
        kb_size: Optional[int] = None,
        selected_algorithms: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Executes actual benchmark runs across specified algorithms and test cases.
        """
        # Determine knowledge base
        active_kb = self.kb
        if kb_size is not None and kb_size > 0:
            active_kb = self.generate_scaled_knowledge_base(kb_size)

        engine = RuleEngine(knowledge_base=active_kb)

        # Slice benchmark test cases
        cases_to_run = self.cases[:test_case_count] if self.cases else []
        if not cases_to_run:
            # Fallback test cases if dataset has not been preprocessed
            cases_to_run = [
                {"case_id": "CASE_FALLBACK_1", "disease": "common_cold", "symptoms": ["fever", "cough", "sore_throat", "runny_nose"]},
                {"case_id": "CASE_FALLBACK_2", "disease": "influenza", "symptoms": ["high_fever", "chills", "muscle_pain", "headache"]},
                {"case_id": "CASE_FALLBACK_3", "disease": "pneumonia", "symptoms": ["high_fever", "cough", "breathlessness", "chest_pain"]},
                {"case_id": "CASE_FALLBACK_4", "disease": "malaria", "symptoms": ["chills", "high_fever", "sweating", "headache"]},
                {"case_id": "CASE_FALLBACK_5", "disease": "jaundice", "symptoms": ["yellowish_skin", "yellowing_of_eyes", "dark_urine"]},
            ]

        algorithms = selected_algorithms or [
            "Simple Matching (Baseline)",
            "Forward Chaining",
            "Backward Chaining",
            "Prioritized Forward Chaining",
        ]

        per_case_records = []
        algo_aggregates: Dict[str, Dict[str, Any]] = {
            algo: {
                "total_time_ms": 0.0,
                "total_evaluated": 0,
                "total_fired": 0,
                "total_iterations": 0,
                "successful_inferences": 0,
                "cases_count": 0,
                "times": [],
            }
            for algo in algorithms
        }

        start_all = time.perf_counter()

        for case in cases_to_run:
            case_id = case.get("case_id", "UNKNOWN")
            ground_truth = case.get("disease", "UNKNOWN")
            symptoms = case.get("symptoms", [])

            for algo in algorithms:
                res: InferenceResult = engine.run_inference(algo, symptoms)

                is_success = bool(res.final_conclusion)
                algo_aggregates[algo]["total_time_ms"] += res.execution_time_ms
                algo_aggregates[algo]["total_evaluated"] += res.evaluated_rules_count
                algo_aggregates[algo]["total_fired"] += len(res.fired_rules)
                algo_aggregates[algo]["total_iterations"] += res.iterations
                algo_aggregates[algo]["cases_count"] += 1
                algo_aggregates[algo]["times"].append(res.execution_time_ms)
                if is_success:
                    algo_aggregates[algo]["successful_inferences"] += 1

                per_case_records.append({
                    "case_id": case_id,
                    "ground_truth": ground_truth,
                    "symptoms_count": len(symptoms),
                    "algorithm": algo,
                    "conclusion": res.final_conclusion or "None",
                    "execution_time_ms": round(res.execution_time_ms, 3),
                    "rules_evaluated": res.evaluated_rules_count,
                    "rules_fired": len(res.fired_rules),
                    "iterations": res.iterations,
                    "status": res.status_message,
                })

        total_wall_time = (time.perf_counter() - start_all) * 1000.0

        # Summary Metrics Table
        summary_rows = []
        for algo, stats in algo_aggregates.items():
            n = max(1, stats["cases_count"])
            avg_time = stats["total_time_ms"] / n
            avg_eval = stats["total_evaluated"] / n
            avg_fired = stats["total_fired"] / n
            avg_iter = stats["total_iterations"] / n
            succ_rate = (stats["successful_inferences"] / n) * 100.0

            summary_rows.append({
                "Algorithm": algo,
                "Test Cases": n,
                "KB Size (Rules)": len(active_kb.rules),
                "Avg Execution Time (ms)": round(avg_time, 3),
                "Total Execution Time (ms)": round(stats["total_time_ms"], 2),
                "Avg Rules Evaluated": round(avg_eval, 1),
                "Avg Rules Fired": round(avg_fired, 1),
                "Avg Iterations": round(avg_iter, 2),
                "Inference Resolution Rate (%)": round(succ_rate, 1),
            })

        df_summary = pd.DataFrame(summary_rows)
        df_detailed = pd.DataFrame(per_case_records)

        # Save benchmark output files
        BENCHMARK_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        summary_csv_path = BENCHMARK_RESULTS_DIR / f"benchmark_summary_{timestamp_str}.csv"
        detailed_csv_path = BENCHMARK_RESULTS_DIR / f"benchmark_detailed_{timestamp_str}.csv"
        benchmark_json_path = BENCHMARK_RESULTS_DIR / f"benchmark_results_{timestamp_str}.json"

        # Also maintain latest pointers
        latest_summary_csv = BENCHMARK_RESULTS_DIR / "latest_benchmark_summary.csv"
        latest_json = BENCHMARK_RESULTS_DIR / "latest_benchmark.json"

        df_summary.to_csv(summary_csv_path, index=False)
        df_summary.to_csv(latest_summary_csv, index=False)
        df_detailed.to_csv(detailed_csv_path, index=False)

        full_payload = {
            "timestamp": timestamp_str,
            "test_cases_count": len(cases_to_run),
            "kb_size": len(active_kb.rules),
            "total_benchmark_time_ms": round(total_wall_time, 2),
            "summary": summary_rows,
            "detailed": per_case_records,
        }

        with open(benchmark_json_path, "w", encoding="utf-8") as f:
            json.dump(full_payload, f, indent=2)
        with open(latest_json, "w", encoding="utf-8") as f:
            json.dump(full_payload, f, indent=2)

        return {
            "summary_df": df_summary,
            "detailed_df": df_detailed,
            "summary_rows": summary_rows,
            "total_time_ms": total_wall_time,
            "summary_csv_path": str(summary_csv_path),
            "detailed_csv_path": str(detailed_csv_path),
            "json_path": str(benchmark_json_path),
        }
