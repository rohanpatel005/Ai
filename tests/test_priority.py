"""
Unit tests for Prioritized Forward Chaining Engine.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.prioritized_forward import PrioritizedForwardChainingEngine


@pytest.fixture
def priority_engine():
    kb = KnowledgeBase()
    return PrioritizedForwardChainingEngine(kb, alpha=0.40, beta=0.35, gamma=0.25)


def test_priority_calculation(priority_engine):
    rule = priority_engine.kb.rules[0]
    score, norm_spec, rel = priority_engine.calculate_rule_priority(rule, set(rule.conditions))
    assert 0.0 <= score <= 1.0
    assert norm_spec <= 1.0
    assert rel == 1.0  # 100% premise overlap


def test_prioritized_inference_success(priority_engine):
    symptoms = ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"]
    res = priority_engine.infer(symptoms)
    assert res.final_conclusion == "common_cold"
    assert len(res.fired_rules) >= 2
    assert res.trace[0].calculated_priority is not None
