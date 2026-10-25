"""
Unit tests for Forward Chaining AI Reasoning Engine.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.forward_chaining import ForwardChainingEngine


@pytest.fixture
def forward_engine():
    kb = KnowledgeBase()
    return ForwardChainingEngine(kb)


def test_forward_empty_input(forward_engine):
    res = forward_engine.infer([])
    assert len(res.inferred_facts) == 0
    assert len(res.fired_rules) == 0
    assert res.final_conclusion is None


def test_forward_single_hop_inference(forward_engine):
    # Rule R_INT_01: fever, cough, sore_throat -> upper_respiratory_syndrome
    res = forward_engine.infer(["fever", "cough", "sore_throat"])
    assert "upper_respiratory_syndrome" in res.inferred_facts
    assert any(r.rule_id == "R_INT_01" for r in res.fired_rules)
    assert res.iterations >= 1


def test_forward_multi_hop_chaining(forward_engine):
    # fever, cough, sore_throat -> upper_respiratory_syndrome
    # upper_respiratory_syndrome + runny_nose + continuous_sneezing -> common_cold
    res = forward_engine.infer(["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"])
    assert "upper_respiratory_syndrome" in res.inferred_facts
    assert "common_cold" in res.inferred_facts
    assert res.final_conclusion == "common_cold"
    assert len(res.fired_rules) >= 2


def test_forward_target_early_termination(forward_engine):
    res = forward_engine.infer(
        ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"],
        target_hypothesis="upper_respiratory_syndrome",
    )
    assert "upper_respiratory_syndrome" in res.inferred_facts
