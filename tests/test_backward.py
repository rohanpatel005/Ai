"""
Unit tests for Backward Chaining AI Reasoning Engine.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.backward_chaining import BackwardChainingEngine


@pytest.fixture
def backward_engine():
    kb = KnowledgeBase()
    return BackwardChainingEngine(kb)


def test_backward_direct_proof(backward_engine):
    # Rule R_VECT_02: chills, vomiting, high_fever, sweating, headache -> malaria
    symptoms = ["chills", "vomiting", "high_fever", "sweating", "headache"]
    res = backward_engine.infer(symptoms, target_hypothesis="malaria")
    assert res.final_conclusion == "malaria"
    assert res.backward_tree is not None
    assert len(res.fired_rules) > 0


def test_backward_multi_hop_proof(backward_engine):
    # Requires establishing intermediate upper_respiratory_syndrome
    symptoms = ["fever", "cough", "sore_throat", "runny_nose", "continuous_sneezing"]
    res = backward_engine.infer(symptoms, target_hypothesis="common_cold")
    assert res.final_conclusion == "common_cold"
    assert "common_cold" in res.inferred_facts


def test_backward_unprovable_goal(backward_engine):
    # Insufficient symptoms to prove malaria
    symptoms = ["headache"]
    res = backward_engine.infer(symptoms, target_hypothesis="malaria")
    assert res.final_conclusion != "malaria"
