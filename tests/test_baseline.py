"""
Unit tests for Simple Symptom Matching Baseline.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.baseline import SimpleSymptomMatcher


@pytest.fixture
def kb():
    return KnowledgeBase()


@pytest.fixture
def matcher(kb):
    return SimpleSymptomMatcher(kb)


def test_baseline_empty_input(matcher):
    result = matcher.match([])
    assert result.evaluated_rules_count > 0
    assert len(result.fired_rules) == 0
    assert result.final_conclusion is None


def test_baseline_matching_ratio(matcher):
    # Rule R_INT_01 requires: fever, cough, sore_throat
    result = matcher.match(["fever", "cough", "sore_throat"], threshold=0.5)
    assert len(result.fired_rules) > 0
    assert any(r.rule_id == "R_INT_01" for r in result.fired_rules)
    assert result.execution_time_ms > 0


def test_baseline_threshold_filtering(matcher):
    # Only 1 symptom matched out of 4 should be below 0.5 threshold
    result = matcher.match(["fever"], threshold=0.8)
    assert all(h.matching_ratio >= 0.8 for h in result.supported_hypotheses)
