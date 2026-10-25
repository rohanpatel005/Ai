"""
Forward Chaining AI Inference Engine (Data-Driven Reasoning).
Implemented from scratch with multi-hop intermediate inference, cycle detection,
and detailed step-by-step reasoning traces.
"""

import time
from typing import List, Dict, Any, Optional, Set

from config import MAX_INFERENCE_ITERATIONS
from src.models import (
    Rule,
    ReasoningStep,
    HypothesisScore,
    InferenceResult,
)
from src.knowledge_base import KnowledgeBase


class ForwardChainingEngine:
    """
    Classical Forward Chaining AI Reasoning Engine.
    Operates data-driven inference: starts with known symptom facts, repeatedly
    evaluates rule premises, fires satisfied rules, and adds deduced conclusions to
    the working memory until a fixpoint is established.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def infer(self, initial_facts: List[str], target_hypothesis: Optional[str] = None) -> InferenceResult:
        """
        Executes standard forward chaining algorithm from scratch.
        """
        start_time = time.perf_counter()

        # Step 1: Initialize facts
        cleaned_facts = [f.strip().lower() for f in initial_facts if f and f.strip()]
        known_facts: Set[str] = set(cleaned_facts)
        newly_inferred_facts: List[str] = []

        fired_rules: List[Rule] = []
        already_fired_rule_ids: Set[str] = set()
        trace: List[ReasoningStep] = []

        total_rules_evaluated = 0
        iterations = 0
        cycle_detected = False
        step_counter = 0

        target_normalized = target_hypothesis.strip().lower() if target_hypothesis else None

        # Step 2: Fixpoint iterative loop
        while iterations < MAX_INFERENCE_ITERATIONS:
            iterations += 1
            changes_in_iteration = False

            # Snapshot of known facts at start of iteration for cycle/growth tracking
            facts_before = len(known_facts)

            for rule in self.kb.rules:
                # If rule already fired and conclusion is already known, skip
                if rule.rule_id in already_fired_rule_ids and rule.conclusion in known_facts:
                    continue

                total_rules_evaluated += 1
                step_counter += 1

                rule_conditions = [c.strip().lower() for c in rule.conditions]
                satisfied = [c for c in rule_conditions if c in known_facts]
                unsatisfied = [c for c in rule_conditions if c not in known_facts]

                is_satisfied = len(unsatisfied) == 0

                if is_satisfied:
                    # Fire rule
                    already_fired_rule_ids.add(rule.rule_id)
                    fired_rules.append(rule)

                    is_new_fact = rule.conclusion not in known_facts
                    if is_new_fact:
                        known_facts.add(rule.conclusion)
                        newly_inferred_facts.append(rule.conclusion)
                        changes_in_iteration = True

                    step = ReasoningStep(
                        step_number=step_counter,
                        rule_id=rule.rule_id,
                        rule_description=rule.description,
                        conditions_evaluated=rule_conditions,
                        satisfied_conditions=satisfied,
                        unsatisfied_conditions=[],
                        fired=True,
                        inferred_fact=rule.conclusion,
                        reason=(
                            f"All {len(rule_conditions)} conditions satisfied. "
                            f"{'Added new fact: ' + rule.conclusion if is_new_fact else 'Conclusion already present in memory.'}"
                        ),
                    )
                    trace.append(step)

                    # Early termination if user specified a target and it has been established
                    if target_normalized and target_normalized in known_facts:
                        break
                else:
                    step = ReasoningStep(
                        step_number=step_counter,
                        rule_id=rule.rule_id,
                        rule_description=rule.description,
                        conditions_evaluated=rule_conditions,
                        satisfied_conditions=satisfied,
                        unsatisfied_conditions=unsatisfied,
                        fired=False,
                        inferred_fact=None,
                        reason=f"Unsatisfied conditions: {', '.join(unsatisfied)}",
                    )
                    trace.append(step)

            # Early termination condition for target
            if target_normalized and target_normalized in known_facts:
                break

            # If no new conclusions were added during this full pass, fixpoint reached
            if not changes_in_iteration:
                break

        if iterations >= MAX_INFERENCE_ITERATIONS:
            cycle_detected = True

        # Step 3: Compile supported hypotheses
        # Differentiate intermediate syndromic facts from terminal diagnoses
        hypothesis_map: Dict[str, Dict[str, Any]] = {}
        for rule in fired_rules:
            conc = rule.conclusion
            if conc not in hypothesis_map:
                hypothesis_map[conc] = {
                    "supporting_rules": [],
                    "matched_conditions": set(),
                    "total_weight": 0.0,
                    "max_priority": 0.0,
                    "sources": set(),
                }
            hypothesis_map[conc]["supporting_rules"].append(rule)
            hypothesis_map[conc]["matched_conditions"].update([c.strip().lower() for c in rule.conditions])
            hypothesis_map[conc]["total_weight"] += rule.evidence_weight
            hypothesis_map[conc]["max_priority"] = max(hypothesis_map[conc]["max_priority"], rule.priority)
            hypothesis_map[conc]["sources"].add(rule.source)

        supported_hypotheses: List[HypothesisScore] = []
        for conc, data in hypothesis_map.items():
            avg_weight = data["total_weight"] / len(data["supporting_rules"])
            score = HypothesisScore(
                hypothesis=conc,
                supporting_rules=data["supporting_rules"],
                matched_conditions=sorted(list(data["matched_conditions"])),
                missing_conditions=[],
                matching_ratio=1.0,  # All conditions were proven
                total_evidence_weight=round(avg_weight, 3),
                max_priority=round(data["max_priority"], 3),
                confidence_descriptor=f"Logical Proof (100% Premise Satisfaction)",
                sources=sorted(list(data["sources"])),
            )
            supported_hypotheses.append(score)

        # Prioritize terminal disease hypotheses over intermediate syndromes
        supported_hypotheses.sort(
            key=lambda h: (
                0 if "syndrome" in h.hypothesis else 1,
                h.total_evidence_weight,
                h.max_priority,
            ),
            reverse=True,
        )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        final_conclusion = supported_hypotheses[0].hypothesis if supported_hypotheses else None
        if cycle_detected:
            status = "Cycle detected in the knowledge base. Inference was safely terminated."
        elif supported_hypotheses:
            status = f"Inferred {len(newly_inferred_facts)} fact(s) across {iterations} iteration(s)."
        else:
            status = "Insufficient information for a rule-based inference."

        return InferenceResult(
            algorithm="Forward Chaining",
            initial_facts=cleaned_facts,
            inferred_facts=newly_inferred_facts,
            all_facts=sorted(list(known_facts)),
            fired_rules=fired_rules,
            evaluated_rules_count=total_rules_evaluated,
            iterations=iterations,
            execution_time_ms=elapsed_ms,
            trace=trace,
            supported_hypotheses=supported_hypotheses,
            final_conclusion=final_conclusion,
            status_message=status,
            cycle_detected=cycle_detected,
        )
