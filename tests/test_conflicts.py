"""
Unit tests for Conflict Resolution and Differential Diagnosis Analysis.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.forward_chaining import ForwardChainingEngine
from src.conflict_resolution import ConflictResolver


def test_conflict_detection_multi_hypothesis():
    kb = KnowledgeBase()
    engine = ForwardChainingEngine(kb)
    # fever, fatigue, headache satisfies both viral_fever and acute_systemic_fatigue_syndrome
    res = engine.infer(["fever", "fatigue", "headache"])
    conflict = ConflictResolver.analyze_conflicts(res)

    assert conflict["has_conflict"] is True
    assert conflict["hypotheses_count"] >= 2
    assert len(conflict["differential_list"]) >= 2
    # Ensure neither hypothesis was silently suppressed
    hypos = [item["hypothesis"] for item in conflict["differential_list"]]
    assert "viral_fever" in hypos
    assert "acute_systemic_fatigue_syndrome" in hypos


def test_unambiguous_inference_no_conflict():
    kb = KnowledgeBase()
    engine = ForwardChainingEngine(kb)
    # Clear malaria symptoms
    res = engine.infer(["chills", "vomiting", "high_fever", "sweating", "headache"])
    conflict = ConflictResolver.analyze_conflicts(res)
    assert conflict["has_conflict"] is False
    assert conflict["hypotheses_count"] == 1
