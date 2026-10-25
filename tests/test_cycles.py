"""
Unit tests for Cycle Detection and Graph Analysis.
"""

import pytest
from src.knowledge_base import KnowledgeBase
from src.cycle_detection import CycleDetector
from src.forward_chaining import ForwardChainingEngine
from src.backward_chaining import BackwardChainingEngine


def test_main_kb_is_acyclic():
    kb = KnowledgeBase()
    detector = CycleDetector(kb)
    report = detector.get_cycle_report()
    assert report["has_cycles"] is False
    assert report["cycle_count"] == 0


def test_viva_demonstration_cycle_detected():
    cyclic_kb = CycleDetector.create_viva_demonstration_cycle_kb()
    detector = CycleDetector(cyclic_kb)
    report = detector.get_cycle_report()
    assert report["has_cycles"] is True
    assert report["cycle_count"] >= 1


def test_backward_chaining_cycle_termination():
    cyclic_kb = CycleDetector.create_viva_demonstration_cycle_kb()
    engine = BackwardChainingEngine(cyclic_kb)
    # Target in recursive cycle loop with no initial facts
    res = engine.infer(initial_facts=[], target_hypothesis="fever_alpha")
    assert res.cycle_detected is True
    assert "Cycle detected" in res.status_message
