"""
Unit tests for Edge Cases, Out-of-Vocabulary Tokens, and Scaled Knowledge Bases.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.rule_engine import RuleEngine
from src.evaluation import ErrorAnalyzer


@pytest.fixture
def rule_engine():
    kb = KnowledgeBase()
    return RuleEngine(kb)


def test_out_of_vocabulary_symptoms(rule_engine):
    res = rule_engine.run_inference("Forward Chaining", ["alien_glow", "spectral_aura"])
    assert len(res.fired_rules) == 0
    assert res.final_conclusion is None
    assert "Insufficient information" in res.status_message


def test_duplicate_symptoms_handling(rule_engine):
    # Redundant symptoms in working memory
    symptoms = ["fever", "fever", "cough", "cough", "sore_throat", "fever"]
    res = rule_engine.run_inference("Forward Chaining", symptoms)
    assert "upper_respiratory_syndrome" in res.inferred_facts


def test_all_14_academic_scenarios_pass():
    analyzer = ErrorAnalyzer()
    results = analyzer.run_all_scenarios()
    assert len(results) == 14
    for r in results:
        assert r["passed"] is True, f"Scenario #{r['id']} ({r['title']}) failed!"
