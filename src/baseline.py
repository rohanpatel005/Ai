"""
Baseline Simple Symptom Matching Engine.
Evaluates direct condition overlap without multi-hop chaining.
Serves as the classical benchmark against which formal AI reasoning is evaluated.
"""

import time
from typing import List, Dict, Any, Optional

from src.models import (
    Rule,
    ReasoningStep,
    HypothesisScore,
    InferenceResult,
)
from src.knowledge_base import KnowledgeBase


class SimpleSymptomMatcher:
    """
    Genuine baseline implementation: calculates direct condition matching ratio
    (matched_conditions / total_conditions) across all rules in the knowledge base.
    Does NOT infer intermediate facts or perform recursive chaining.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def match(self, input_symptoms: List[str], threshold: float = 0.5) -> InferenceResult:
        """
        Executes baseline symptom matching.
        """
        start_time = time.perf_counter()

        cleaned_inputs = [s.strip().lower() for s in input_symptoms if s and s.strip()]
        input_set = set(cleaned_inputs)

        trace: List[ReasoningStep] = []
        hypothesis_map: Dict[str, Dict[str, Any]] = {}
        rules_evaluated = 0
        fired_rules: List[Rule] = []

        for idx, rule in enumerate(self.kb.rules):
            rules_evaluated += 1
            rule_conditions = [c.strip().lower() for c in rule.conditions]
            satisfied = [c for c in rule_conditions if c in input_set]
            unsatisfied = [c for c in rule_conditions if c not in input_set]

            ratio = len(satisfied) / len(rule_conditions) if rule_conditions else 0.0

            # Direct firing in baseline if threshold met
            is_fired = ratio >= threshold

            step = ReasoningStep(
                step_number=idx + 1,
                rule_id=rule.rule_id,
                rule_description=rule.description,
                conditions_evaluated=rule_conditions,
                satisfied_conditions=satisfied,
                unsatisfied_conditions=unsatisfied,
                fired=is_fired,
                inferred_fact=rule.conclusion if is_fired else None,
                reason=(
                    f"Baseline overlap ratio: {len(satisfied)}/{len(rule_conditions)} ({ratio:.2f}) "
                    f"- {'Exceeds' if is_fired else 'Below'} threshold {threshold:.2f}"
                ),
            )
            trace.append(step)

            if is_fired:
                fired_rules.append(rule)
                conc = rule.conclusion
                if conc not in hypothesis_map:
                    hypothesis_map[conc] = {
                        "supporting_rules": [],
                        "matched_conditions": set(),
                        "missing_conditions": set(),
                        "total_weight": 0.0,
                        "max_priority": 0.0,
                        "max_ratio": 0.0,
                        "sources": set(),
                    }
                hypothesis_map[conc]["supporting_rules"].append(rule)
                hypothesis_map[conc]["matched_conditions"].update(satisfied)
                hypothesis_map[conc]["missing_conditions"].update(unsatisfied)
                hypothesis_map[conc]["total_weight"] += rule.evidence_weight
                hypothesis_map[conc]["max_priority"] = max(hypothesis_map[conc]["max_priority"], rule.priority)
                hypothesis_map[conc]["max_ratio"] = max(hypothesis_map[conc]["max_ratio"], ratio)
                hypothesis_map[conc]["sources"].add(rule.source)

        # Assemble supported hypotheses
        supported_hypotheses: List[HypothesisScore] = []
        for conc, data in hypothesis_map.items():
            avg_weight = data["total_weight"] / len(data["supporting_rules"])
            score = HypothesisScore(
                hypothesis=conc,
                supporting_rules=data["supporting_rules"],
                matched_conditions=sorted(list(data["matched_conditions"])),
                missing_conditions=sorted(list(data["missing_conditions"])),
                matching_ratio=round(data["max_ratio"], 3),
                total_evidence_weight=round(avg_weight, 3),
                max_priority=round(data["max_priority"], 3),
                confidence_descriptor=f"Direct Overlap: {data['max_ratio'] * 100:.1f}%",
                sources=sorted(list(data["sources"])),
            )
            supported_hypotheses.append(score)

        # Sort hypotheses by matching ratio descending
        supported_hypotheses.sort(key=lambda h: (h.matching_ratio, h.total_evidence_weight), reverse=True)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        final_conclusion = supported_hypotheses[0].hypothesis if supported_hypotheses else None
        status = "Supported hypotheses found" if supported_hypotheses else "Insufficient symptom overlap"

        return InferenceResult(
            algorithm="Simple Symptom Matching (Baseline)",
            initial_facts=cleaned_inputs,
            inferred_facts=[h.hypothesis for h in supported_hypotheses],
            all_facts=cleaned_inputs + [h.hypothesis for h in supported_hypotheses],
            fired_rules=fired_rules,
            evaluated_rules_count=rules_evaluated,
            iterations=1,
            execution_time_ms=elapsed_ms,
            trace=trace,
            supported_hypotheses=supported_hypotheses,
            final_conclusion=final_conclusion,
            status_message=status,
            cycle_detected=False,
        )
