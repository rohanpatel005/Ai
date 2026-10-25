"""
Data models and type definitions for the Medical Expert System.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Rule:
    """
    Formal representation of an IF-THEN medical rule.
    """
    rule_id: str
    conditions: List[str]
    conclusion: str
    evidence_weight: float
    specificity: int
    priority: float
    source: str
    source_url: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "conditions": self.conditions,
            "conclusion": self.conclusion,
            "evidence_weight": self.evidence_weight,
            "specificity": self.specificity,
            "priority": self.priority,
            "source": self.source,
            "source_url": self.source_url,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rule":
        conditions = data.get("conditions", [])
        if isinstance(conditions, str):
            # Handle comma-separated condition string
            conditions = [c.strip().lower() for c in conditions.split(",") if c.strip()]
        else:
            conditions = [str(c).strip().lower() for c in conditions if str(c).strip()]

        return cls(
            rule_id=str(data.get("rule_id", "")).strip(),
            conditions=conditions,
            conclusion=str(data.get("conclusion", "")).strip().lower(),
            evidence_weight=float(data.get("evidence_weight", 0.5)),
            specificity=int(data.get("specificity", len(conditions))),
            priority=float(data.get("priority", 0.5)),
            source=str(data.get("source", "Standard Reference")).strip(),
            source_url=str(data.get("source_url", "")).strip(),
            description=str(data.get("description", "")).strip(),
        )


@dataclass
class ReasoningStep:
    """
    Record of a single reasoning step for explainability.
    """
    step_number: int
    rule_id: str
    rule_description: str
    conditions_evaluated: List[str]
    satisfied_conditions: List[str]
    unsatisfied_conditions: List[str]
    fired: bool
    inferred_fact: Optional[str]
    reason: str
    calculated_priority: Optional[float] = None


@dataclass
class BackwardGoalNode:
    """
    Node in the Backward Chaining goal tree.
    """
    goal: str
    status: str  # "PROVEN_FACT", "PROVEN_RULE", "FAILED", "CYCLE_DETECTED"
    rule_id: Optional[str] = None
    children: List["BackwardGoalNode"] = field(default_factory=list)
    depth: int = 0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "status": self.status,
            "rule_id": self.rule_id,
            "depth": self.depth,
            "message": self.message,
            "children": [c.to_dict() for c in self.children],
        }


@dataclass
class HypothesisScore:
    """
    Hypothesis evaluated with supporting rules and metrics.
    """
    hypothesis: str
    supporting_rules: List[Rule]
    matched_conditions: List[str]
    missing_conditions: List[str]
    matching_ratio: float
    total_evidence_weight: float
    max_priority: float
    confidence_descriptor: str
    sources: List[str]


@dataclass
class InferenceResult:
    """
    Complete outcome of an AI reasoning run.
    """
    algorithm: str
    initial_facts: List[str]
    inferred_facts: List[str]
    all_facts: List[str]
    fired_rules: List[Rule]
    evaluated_rules_count: int
    iterations: int
    execution_time_ms: float
    trace: List[ReasoningStep]
    supported_hypotheses: List[HypothesisScore]
    final_conclusion: Optional[str]
    status_message: str
    cycle_detected: bool = False
    backward_tree: Optional[BackwardGoalNode] = None
    memory_usage_kb: float = 0.0

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "Algorithm": self.algorithm,
            "Initial Facts": len(self.initial_facts),
            "Inferred Facts": len(self.inferred_facts),
            "Fired Rules": len(self.fired_rules),
            "Evaluated Rules": self.evaluated_rules_count,
            "Iterations": self.iterations,
            "Execution Time (ms)": round(self.execution_time_ms, 3),
            "Conclusion": self.final_conclusion or "None",
            "Status": self.status_message,
        }
