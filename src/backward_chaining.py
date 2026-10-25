"""
Backward Chaining AI Inference Engine (Goal-Driven Reasoning).
Implemented from scratch with recursive sub-goal resolution, visited-set cycle detection,
and interactive goal-tree generation.
"""

import time
from typing import List, Dict, Any, Optional, Set, Tuple

from config import MAX_BACKWARD_DEPTH
from src.models import (
    Rule,
    ReasoningStep,
    HypothesisScore,
    InferenceResult,
    BackwardGoalNode,
)
from src.knowledge_base import KnowledgeBase


class BackwardChainingEngine:
    """
    Classical Backward Chaining AI Reasoning Engine.
    Operates goal-driven deduction: starts from a target hypothesis (or searches
    promising hypotheses), recursively seeks rules that conclude the target,
    and attempts to verify premise conditions against known facts or sub-goals.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def infer(self, initial_facts: List[str], target_hypothesis: Optional[str] = None) -> InferenceResult:
        """
        Executes backward chaining to establish a target hypothesis or rank potential hypotheses.
        """
        start_time = time.perf_counter()

        cleaned_facts = [f.strip().lower() for f in initial_facts if f and f.strip()]
        known_facts: Set[str] = set(cleaned_facts)
        newly_proven_facts: Set[str] = set()

        fired_rules: List[Rule] = []
        fired_rule_ids: Set[str] = set()
        trace: List[ReasoningStep] = []
        rules_evaluated_count = 0
        step_counter = 0
        global_cycle_detected = False

        # If no specific target hypothesis is provided, identify candidates from KB
        candidate_goals: List[str] = []
        if target_hypothesis and target_hypothesis.strip():
            candidate_goals = [target_hypothesis.strip().lower()]
        else:
            # Rank candidates by condition overlap with initial facts
            scores = []
            for conc in self.kb.get_all_conclusions():
                rules = self.kb.get_rules_by_conclusion(conc)
                overlap = sum(1 for r in rules for c in r.conditions if c in known_facts)
                scores.append((conc, overlap))
            scores.sort(key=lambda x: x[1], reverse=True)
            candidate_goals = [s[0] for s in scores if s[1] > 0]
            if not candidate_goals:
                candidate_goals = self.kb.get_all_conclusions()[:10]

        # Recursive goal prover
        def prove_goal(
            goal: str,
            current_known: Set[str],
            visited_path: Set[str],
            depth: int
        ) -> Tuple[bool, BackwardGoalNode]:
            nonlocal step_counter, rules_evaluated_count, global_cycle_detected

            goal_norm = goal.strip().lower()

            # Base Case 1: Already proven fact in working memory
            if goal_norm in current_known:
                return True, BackwardGoalNode(
                    goal=goal_norm,
                    status="PROVEN_FACT",
                    depth=depth,
                    message="Directly verified from known facts",
                )

            # Base Case 2: Cycle Detection in current deduction branch
            if goal_norm in visited_path:
                global_cycle_detected = True
                step_counter += 1
                trace.append(ReasoningStep(
                    step_number=step_counter,
                    rule_id="CYCLE_GUARD",
                    rule_description=f"Cycle detected for sub-goal '{goal_norm}'",
                    conditions_evaluated=[goal_norm],
                    satisfied_conditions=[],
                    unsatisfied_conditions=[goal_norm],
                    fired=False,
                    inferred_fact=None,
                    reason=f"Sub-goal '{goal_norm}' is already on the current proof path: {list(visited_path)}",
                ))
                return False, BackwardGoalNode(
                    goal=goal_norm,
                    status="CYCLE_DETECTED",
                    depth=depth,
                    message=f"Cycle detected on proof path: {' -> '.join(visited_path)} -> {goal_norm}",
                )

            # Base Case 3: Depth Limit
            if depth >= MAX_BACKWARD_DEPTH:
                return False, BackwardGoalNode(
                    goal=goal_norm,
                    status="FAILED",
                    depth=depth,
                    message=f"Maximum search depth ({MAX_BACKWARD_DEPTH}) reached",
                )

            # Recursive Case: Find rules that conclude this goal
            candidate_rules = self.kb.get_rules_by_conclusion(goal_norm)
            if not candidate_rules:
                return False, BackwardGoalNode(
                    goal=goal_norm,
                    status="FAILED",
                    depth=depth,
                    message="No rule in knowledge base concludes this sub-goal",
                )

            goal_node = BackwardGoalNode(
                goal=goal_norm,
                status="EVALUATING",
                depth=depth,
                message=f"Evaluating {len(candidate_rules)} candidate rule(s)",
            )

            visited_path.add(goal_norm)

            for rule in candidate_rules:
                rules_evaluated_count += 1
                step_counter += 1

                rule_node = BackwardGoalNode(
                    goal=f"Rule: {rule.rule_id}",
                    status="EVALUATING",
                    rule_id=rule.rule_id,
                    depth=depth + 1,
                    message=rule.description,
                )

                rule_conditions = [c.strip().lower() for c in rule.conditions]
                all_conditions_satisfied = True
                satisfied_conds = []
                unsatisfied_conds = []

                for cond in rule_conditions:
                    cond_success, cond_node = prove_goal(
                        cond,
                        current_known,
                        visited_path,
                        depth + 2
                    )
                    rule_node.children.append(cond_node)

                    if cond_success:
                        satisfied_conds.append(cond)
                    else:
                        unsatisfied_conds.append(cond)
                        all_conditions_satisfied = False
                        # Cannot prove this rule; break early to prune
                        break

                if all_conditions_satisfied:
                    # Rule succeeds!
                    rule_node.status = "PROVEN_RULE"
                    rule_node.message = f"All {len(rule_conditions)} conditions verified"
                    goal_node.children.append(rule_node)
                    goal_node.status = "PROVEN_RULE"
                    goal_node.rule_id = rule.rule_id
                    goal_node.message = f"Proved via rule {rule.rule_id}"

                    current_known.add(goal_norm)
                    newly_proven_facts.add(goal_norm)

                    if rule.rule_id not in fired_rule_ids:
                        fired_rule_ids.add(rule.rule_id)
                        fired_rules.append(rule)

                    trace.append(ReasoningStep(
                        step_number=step_counter,
                        rule_id=rule.rule_id,
                        rule_description=rule.description,
                        conditions_evaluated=rule_conditions,
                        satisfied_conditions=satisfied_conds,
                        unsatisfied_conditions=[],
                        fired=True,
                        inferred_fact=goal_norm,
                        reason=f"Backward proof succeeded: all conditions proven for {rule.rule_id}",
                    ))

                    visited_path.remove(goal_norm)
                    return True, goal_node
                else:
                    rule_node.status = "FAILED"
                    rule_node.message = f"Failed to prove condition: {unsatisfied_conds[0] if unsatisfied_conds else 'Unknown'}"
                    goal_node.children.append(rule_node)

                    trace.append(ReasoningStep(
                        step_number=step_counter,
                        rule_id=rule.rule_id,
                        rule_description=rule.description,
                        conditions_evaluated=rule_conditions,
                        satisfied_conditions=satisfied_conds,
                        unsatisfied_conditions=unsatisfied_conds,
                        fired=False,
                        inferred_fact=None,
                        reason=f"Backward proof failed: could not establish condition {unsatisfied_conds[0] if unsatisfied_conds else ''}",
                    ))

            visited_path.remove(goal_norm)
            goal_node.status = "FAILED"
            goal_node.message = "All candidate rules failed to establish required conditions"
            return False, goal_node

        # Root proof coordinator
        root_tree = BackwardGoalNode(
            goal="Target Hypothesis Exploration" if len(candidate_goals) > 1 else candidate_goals[0],
            status="ROOT",
            depth=0,
            message=f"Exploring {len(candidate_goals)} target hypothesis branch(es)",
        )

        proven_goals: List[str] = []
        for target in candidate_goals:
            target_success, target_node = prove_goal(
                target,
                known_facts,
                set(),
                1
            )
            root_tree.children.append(target_node)
            if target_success:
                proven_goals.append(target)

        # Assemble supported hypotheses
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
                confidence_descriptor="Goal Verified via Backward Deduction",
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

        if global_cycle_detected:
            status = "Cycle detected in the knowledge base. Inference was safely terminated."
        elif supported_hypotheses:
            status = f"Successfully proved {len(proven_goals)} hypothesis goal(s)."
        else:
            status = "Target hypothesis could not be established from current facts."

        return InferenceResult(
            algorithm="Backward Chaining",
            initial_facts=cleaned_facts,
            inferred_facts=sorted(list(newly_proven_facts)),
            all_facts=sorted(list(known_facts)),
            fired_rules=fired_rules,
            evaluated_rules_count=rules_evaluated_count,
            iterations=len(candidate_goals),
            execution_time_ms=elapsed_ms,
            trace=trace,
            supported_hypotheses=supported_hypotheses,
            final_conclusion=final_conclusion,
            status_message=status,
            cycle_detected=global_cycle_detected,
            backward_tree=root_tree,
        )
