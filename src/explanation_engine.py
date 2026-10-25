"""
Explanation Engine Module.
Generates human-readable, transparent, and defensible WHY and HOW reasoning traces.
"""

from typing import List, Dict, Any, Optional
import pandas as pd

from src.models import InferenceResult, ReasoningStep, Rule


class ExplanationEngine:
    """
    Translates raw symbolic execution traces into structured, transparent,
    and defensible medical AI explanations.
    """

    @staticmethod
    def generate_narrative_explanation(result: InferenceResult) -> Dict[str, Any]:
        """
        Creates a structured narrative explanation answering WHAT, WHY, and HOW.
        """
        facts_str = ", ".join(result.initial_facts) if result.initial_facts else "None provided"
        inferred_str = ", ".join(result.inferred_facts) if result.inferred_facts else "None"

        # WHAT happened
        what_summary = (
            f"The {result.algorithm} evaluated {result.evaluated_rules_count} rule premises "
            f"over {result.iterations} reasoning pass(es), successfully firing {len(result.fired_rules)} rule(s) "
            f"in {result.execution_time_ms:.2f} ms."
        )

        # WHY conclusions were established
        why_bullets = []
        for rule in result.fired_rules:
            conds_str = " AND ".join(rule.conditions)
            why_bullets.append(
                f"Rule [{rule.rule_id}]: Because premises ({conds_str}) were fully verified, "
                f"the system deduced '{rule.conclusion}' [Source: {rule.source}]."
            )

        if not why_bullets:
            why_bullets.append(
                "No rule premises were completely satisfied by the entered symptoms. "
                "Insufficient evidence exists in the current knowledge base."
            )

        # HOW: Chaining stages
        how_stages = []
        how_stages.append({
            "stage": 1,
            "title": "Initial Working Memory",
            "content": f"User entered facts: {facts_str}",
        })

        if result.inferred_facts:
            # Group intermediate vs terminal
            intermediates = [f for f in result.inferred_facts if "syndrome" in f]
            terminals = [f for f in result.inferred_facts if "syndrome" not in f]

            if intermediates:
                how_stages.append({
                    "stage": 2,
                    "title": "Intermediate Syndromic Abstractions",
                    "content": f"Multi-hop rules deduced intermediate syndromes: {', '.join(intermediates)}",
                })
            if terminals:
                how_stages.append({
                    "stage": 3,
                    "title": "Terminal Hypothesis Derivation",
                    "content": f"Final supported diagnoses established: {', '.join(terminals)}",
                })
        else:
            how_stages.append({
                "stage": 2,
                "title": "Inference Termination",
                "content": "Premise evaluation completed without any firing.",
            })

        return {
            "algorithm": result.algorithm,
            "what_summary": what_summary,
            "initial_facts": result.initial_facts,
            "inferred_facts": result.inferred_facts,
            "fired_rules_count": len(result.fired_rules),
            "why_explanations": why_bullets,
            "how_chain_stages": how_stages,
            "final_conclusion": result.final_conclusion,
            "status": result.status_message,
        }

    @staticmethod
    def get_steps_dataframe(result: InferenceResult) -> pd.DataFrame:
        """
        Converts the reasoning trace into a clean Pandas DataFrame for UI presentation or CSV download.
        """
        rows = []
        for step in result.trace:
            rows.append({
                "Step #": step.step_number,
                "Rule ID": step.rule_id,
                "Status": "FIRED" if step.fired else "SKIPPED",
                "Conditions Evaluated": ", ".join(step.conditions_evaluated),
                "Satisfied Conditions": ", ".join(step.satisfied_conditions),
                "Unsatisfied Conditions": ", ".join(step.unsatisfied_conditions),
                "Inferred Fact": step.inferred_fact or "-",
                "Priority Score": f"{step.calculated_priority:.3f}" if step.calculated_priority is not None else "-",
                "Reason / Justification": step.reason,
            })
        return pd.DataFrame(rows)
