"""
Unified AI Rule Engine Controller.
Coordinates all four reasoning paradigms and provides side-by-side comparative execution.
"""

from typing import List, Dict, Any, Optional

from src.knowledge_base import KnowledgeBase
from src.baseline import SimpleSymptomMatcher
from src.forward_chaining import ForwardChainingEngine
from src.backward_chaining import BackwardChainingEngine
from src.prioritized_forward import PrioritizedForwardChainingEngine
from src.models import InferenceResult


class RuleEngine:
    """
    Central coordinator managing classical AI reasoning execution across all paradigms:
    1. Simple Symptom Matching (Baseline)
    2. Forward Chaining
    3. Backward Chaining
    4. Prioritized Forward Chaining
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        self.kb = knowledge_base if knowledge_base is not None else KnowledgeBase()
        self.baseline_engine = SimpleSymptomMatcher(self.kb)
        self.forward_engine = ForwardChainingEngine(self.kb)
        self.backward_engine = BackwardChainingEngine(self.kb)
        self.prioritized_engine = PrioritizedForwardChainingEngine(self.kb)

    def run_inference(
        self,
        algorithm: str,
        symptoms: List[str],
        target_hypothesis: Optional[str] = None,
        alpha: Optional[float] = None,
        beta: Optional[float] = None,
        gamma: Optional[float] = None,
    ) -> InferenceResult:
        """
        Executes a single specified reasoning algorithm.
        """
        algo_clean = algorithm.strip().lower()

        if "simple" in algo_clean or "baseline" in algo_clean or "matching" in algo_clean:
            return self.baseline_engine.match(symptoms)

        elif "backward" in algo_clean:
            return self.backward_engine.infer(symptoms, target_hypothesis=target_hypothesis)

        elif "prioritized" in algo_clean:
            return self.prioritized_engine.infer(
                symptoms,
                target_hypothesis=target_hypothesis,
                alpha=alpha,
                beta=beta,
                gamma=gamma,
            )

        else:
            # Default to standard Forward Chaining
            return self.forward_engine.infer(symptoms, target_hypothesis=target_hypothesis)

    def run_all_algorithms(
        self,
        symptoms: List[str],
        target_hypothesis: Optional[str] = None,
        alpha: Optional[float] = None,
        beta: Optional[float] = None,
        gamma: Optional[float] = None,
    ) -> Dict[str, InferenceResult]:
        """
        Runs the exact same symptom input through all 4 algorithms to enable rigorous comparison.
        """
        results = {
            "Simple Matching (Baseline)": self.baseline_engine.match(symptoms),
            "Forward Chaining": self.forward_engine.infer(symptoms, target_hypothesis=target_hypothesis),
            "Backward Chaining": self.backward_engine.infer(symptoms, target_hypothesis=target_hypothesis),
            "Prioritized Forward Chaining": self.prioritized_engine.infer(
                symptoms,
                target_hypothesis=target_hypothesis,
                alpha=alpha,
                beta=beta,
                gamma=gamma,
            ),
        }
        return results
