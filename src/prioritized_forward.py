"""
Prioritized Forward Chaining AI Inference Engine.
Applies domain-specific rule prioritization and inference optimization using
configurable weighting of specificity, evidence weight, and working-memory relevance.
"""

import time
from typing import List, Dict, Any, Optional, Set, Tuple

from config import DEFAULT_ALPHA, DEFAULT_BETA, DEFAULT_GAMMA, MAX_INFERENCE_ITERATIONS
from src.models import (
    Rule,
    ReasoningStep,
    HypothesisScore,
    InferenceResult,
)
from src.knowledge_base import KnowledgeBase


class PrioritizedForwardChainingEngine:
    """
    Optimized Forward Chaining AI Reasoning Engine.
    Uses domain-specific rule prioritization and inference optimization to order
    rule evaluations dynamically based on premise specificity, evidence weight,
    and symptom relevance to working memory.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        alpha: float = DEFAULT_ALPHA,
        beta: float = DEFAULT_BETA,
        gamma: float = DEFAULT_GAMMA,
    ):
        self.kb = knowledge_base
        self.alpha = float(alpha)  # Specificity weight
        self.beta = float(beta)    # Evidence weight
        self.gamma = float(gamma)  # Relevance weight

        # Normalize weights so sum is 1.0 if not zero
        total_w = self.alpha + self.beta + self.gamma
        if total_w > 0:
            self.alpha /= total_w
            self.beta /= total_w
            self.gamma /= total_w

        # Max specificity across knowledge base for normalization
        max_spec = max((r.specificity for r in self.kb.rules), default=1)
        self.max_specificity = max(1, max_spec)

    def calculate_rule_priority(self, rule: Rule, current_known_facts: Set[str]) -> Tuple[float, float, float]:
        """
        Calculates dynamic rule priority score:
        score = alpha * norm_specificity + beta * evidence_weight + gamma * relevance
        """
        norm_spec = min(1.0, rule.specificity / self.max_specificity)
        ev_weight = rule.evidence_weight

        rule_conditions = [c.strip().lower() for c in rule.conditions]
        matched_count = sum(1 for c in rule_conditions if c in current_known_facts)
        relevance = matched_count / len(rule_conditions) if rule_conditions else 0.0

        score = (self.alpha * norm_spec) + (self.beta * ev_weight) + (self.gamma * relevance)
        return round(score, 4), norm_spec, relevance

    def infer(
        self,
        initial_facts: List[str],
        target_hypothesis: Optional[str] = None,
        alpha: Optional[float] = None,
        beta: Optional[float] = None,
        gamma: Optional[float] = None,
    ) -> InferenceResult:
        """
        Executes prioritized forward chaining with dynamic queue sorting and trace collection.
        """
        if alpha is not None:
            self.alpha = alpha
        if beta is not None:
            self.beta = beta
        if gamma is not None:
            self.gamma = gamma

        start_time = time.perf_counter()

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

        while iterations < MAX_INFERENCE_ITERATIONS:
            iterations += 1
            changes_in_iteration = False

            # Dynamic prioritization: rank unfired rules based on current working memory
            candidate_rules_with_priority = []
            for rule in self.kb.rules:
                if rule.rule_id in already_fired_rule_ids and rule.conclusion in known_facts:
                    continue
                score, norm_spec, relevance = self.calculate_rule_priority(rule, known_facts)
                candidate_rules_with_priority.append((rule, score, norm_spec, relevance))

            # Sort descending: highest prioritized rules evaluated first
            candidate_rules_with_priority.sort(key=lambda item: item[1], reverse=True)

            for rule, score, norm_spec, relevance in candidate_rules_with_priority:
                total_rules_evaluated += 1
                step_counter += 1

                rule_conditions = [c.strip().lower() for c in rule.conditions]
                satisfied = [c for c in rule_conditions if c in known_facts]
                unsatisfied = [c for c in rule_conditions if c not in known_facts]

                is_satisfied = len(unsatisfied) == 0

                if is_satisfied:
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
                            f"Priority score: {score:.3f} (Spec={norm_spec:.2f}, Evid={rule.evidence_weight:.2f}, Rel={relevance:.2f}). "
                            f"All conditions satisfied. {'New fact: ' + rule.conclusion if is_new_fact else 'Already known.'}"
                        ),
                        calculated_priority=score,
                    )
                    trace.append(step)

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
                        reason=f"Priority {score:.3f}. Unsatisfied premises: {', '.join(unsatisfied)}",
                        calculated_priority=score,
                    )
                    trace.append(step)

            if target_normalized and target_normalized in known_facts:
                break

            if not changes_in_iteration:
                break

        if iterations >= MAX_INFERENCE_ITERATIONS:
            cycle_detected = True

        # Compile supported hypotheses
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
                matching_ratio=1.0,
                total_evidence_weight=round(avg_weight, 3),
                max_priority=round(data["max_priority"], 3),
                confidence_descriptor="Prioritized Proof (Optimized Evaluation)",
                sources=sorted(list(data["sources"])),
            )
            supported_hypotheses.append(score)

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
            status = f"Inferred {len(newly_inferred_facts)} fact(s) using prioritized ordering across {iterations} iteration(s)."
        else:
            status = "Insufficient information for a rule-based inference."

        return InferenceResult(
            algorithm="Prioritized Forward Chaining",
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
