"""
Conflict Resolution and Differential Diagnosis Analysis Module.
Transparently evaluates and presents competing hypotheses when multiple rules fire.
"""

from typing import List, Dict, Any, Optional

from src.models import HypothesisScore, InferenceResult


class ConflictResolver:
    """
    Manages conflict resolution and multi-hypothesis differential reporting.
    Strictly prevents silent single-hypothesis selection in ambiguous clinical contexts.
    """

    @staticmethod
    def analyze_conflicts(result: InferenceResult) -> Dict[str, Any]:
        """
        Analyzes the inference result for competing hypotheses and returns a structured
        differential diagnosis breakdown.
        """
        hypotheses = result.supported_hypotheses

        if not hypotheses:
            return {
                "has_conflict": False,
                "status": "NO_HYPOTHESIS",
                "message": "Insufficient information for a rule-based inference.",
                "hypotheses_count": 0,
                "differential_list": [],
            }

        # Filter out strictly intermediate syndromic facts for the main differential
        INTERMEDIATE_SYNDROMES = {
            "upper_respiratory_syndrome",
            "lower_respiratory_syndrome",
            "acute_febrile_syndrome",
            "gastrointestinal_syndrome",
            "hepatobiliary_syndrome",
        }
        terminal_hypotheses = [h for h in hypotheses if h.hypothesis not in INTERMEDIATE_SYNDROMES]
        candidates = terminal_hypotheses if terminal_hypotheses else hypotheses

        if len(candidates) == 1:
            return {
                "has_conflict": False,
                "status": "UNAMBIGUOUS_INFERENCE",
                "message": f"Single hypothesis supported: {candidates[0].hypothesis}",
                "hypotheses_count": 1,
                "differential_list": [ConflictResolver._format_hypothesis(candidates[0])],
            }

        # Multiple hypotheses supported -> Conflict / Differential scenario
        differential_list = [ConflictResolver._format_hypothesis(h) for h in candidates]

        # Rank candidates by evidence weight and priority for inspection, without discarding any
        return {
            "has_conflict": True,
            "status": "MULTIPLE_HYPOTHESES_SUPPORTED",
            "message": "Multiple hypotheses are supported by the current knowledge base.",
            "hypotheses_count": len(candidates),
            "differential_list": differential_list,
            "safety_recommendation": (
                "The current knowledge base contains supporting rules for multiple conditions. "
                "Each supported hypothesis below must be individually inspected along with its "
                "supporting evidence, premises, and cited medical source."
            ),
        }

    @staticmethod
    def _format_hypothesis(h: HypothesisScore) -> Dict[str, Any]:
        return {
            "hypothesis": h.hypothesis,
            "supporting_rule_ids": [r.rule_id for r in h.supporting_rules],
            "matched_conditions": h.matched_conditions,
            "missing_conditions": h.missing_conditions,
            "matching_ratio": h.matching_ratio,
            "evidence_weight": h.total_evidence_weight,
            "priority": h.max_priority,
            "confidence_descriptor": h.confidence_descriptor,
            "sources": h.sources,
            "rule_descriptions": [r.description for r in h.supporting_rules],
        }
