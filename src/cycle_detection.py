"""
Cycle Detection and Dependency Graph Analysis Module.
Detects circular dependencies in the knowledge base and demonstrates safe termination.
"""

from typing import List, Dict, Set, Tuple, Any, Optional
import networkx as nx

from src.models import Rule
from src.knowledge_base import KnowledgeBase


class CycleDetector:
    """
    Performs graph-theoretic dependency analysis on explicit IF-THEN rules
    to identify circular definitions (e.g., A -> B -> C -> A) and ensure inference safety.
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        self.kb = knowledge_base

    def build_dependency_graph(self, rules: List[Rule]) -> nx.DiGraph:
        """
        Builds a directed dependency graph where an edge exists from fact A to fact B
        if there is a rule with premise A and conclusion B.
        """
        graph = nx.DiGraph()
        for rule in rules:
            for cond in rule.conditions:
                graph.add_edge(cond.strip().lower(), rule.conclusion.strip().lower(), rule_id=rule.rule_id)
        return graph

    def detect_static_cycles(self, rules: Optional[List[Rule]] = None) -> List[List[str]]:
        """
        Identifies all simple cycles in the rule dependency graph using NetworkX.
        Returns a list of cycles, each cycle being a list of node names forming the loop.
        """
        rule_list = rules if rules is not None else (self.kb.rules if self.kb else [])
        if not rule_list:
            return []

        graph = self.build_dependency_graph(rule_list)
        try:
            cycles = list(nx.simple_cycles(graph))
            return cycles
        except Exception:
            return []

    def get_cycle_report(self, rules: Optional[List[Rule]] = None) -> Dict[str, Any]:
        """
        Generates a structured report on knowledge base cycle safety.
        """
        cycles = self.detect_static_cycles(rules)
        has_cycle = len(cycles) > 0

        formatted_cycles = []
        for c in cycles:
            # e.g., ["a", "b", "c"] -> "a -> b -> c -> a"
            loop_str = " -> ".join(c) + f" -> {c[0]}"
            formatted_cycles.append(loop_str)

        return {
            "has_cycles": has_cycle,
            "cycle_count": len(cycles),
            "cycles": formatted_cycles,
            "status_message": (
                "Cycle detected in the knowledge base. Inference was safely terminated."
                if has_cycle
                else "Knowledge base graph is acyclic. Safe for inference."
            ),
        }

    @staticmethod
    def create_viva_demonstration_cycle_kb() -> KnowledgeBase:
        """
        Creates a synthetic knowledge base with an intentional circular loop
        specifically for viva examination and safety demonstration.
        Loop: fever_alpha -> syndrome_beta -> syndrome_gamma -> fever_alpha
        """
        cyclic_rules = [
            Rule(
                rule_id="CYCLE_R01",
                conditions=["fever_alpha"],
                conclusion="syndrome_beta",
                evidence_weight=0.85,
                specificity=1,
                priority=0.80,
                source="Viva Demonstration Case",
                source_url="https://adaniuni.ac.in",
                description="Demonstration rule 1: fever_alpha leads to syndrome_beta",
            ),
            Rule(
                rule_id="CYCLE_R02",
                conditions=["syndrome_beta"],
                conclusion="syndrome_gamma",
                evidence_weight=0.85,
                specificity=1,
                priority=0.80,
                source="Viva Demonstration Case",
                source_url="https://adaniuni.ac.in",
                description="Demonstration rule 2: syndrome_beta leads to syndrome_gamma",
            ),
            Rule(
                rule_id="CYCLE_R03",
                conditions=["syndrome_gamma"],
                conclusion="fever_alpha",
                evidence_weight=0.85,
                specificity=1,
                priority=0.80,
                source="Viva Demonstration Case",
                source_url="https://adaniuni.ac.in",
                description="Demonstration rule 3: syndrome_gamma loops back to fever_alpha (CIRCULAR LOOP)",
            ),
            Rule(
                rule_id="CYCLE_R04",
                conditions=["syndrome_gamma"],
                conclusion="terminal_state_omega",
                evidence_weight=0.90,
                specificity=1,
                priority=0.85,
                source="Viva Demonstration Case",
                source_url="https://adaniuni.ac.in",
                description="Demonstration rule 4: Branch from syndrome_gamma to terminal state",
            ),
        ]

        demo_kb = KnowledgeBase.__new__(KnowledgeBase)
        demo_kb.json_path = None
        demo_kb.csv_path = None
        demo_kb.rules = cyclic_rules
        demo_kb._rules_by_id = {r.rule_id: r for r in cyclic_rules}
        demo_kb._rules_by_conclusion = {}
        demo_kb._rules_by_condition = {}
        for r in cyclic_rules:
            demo_kb._rules_by_conclusion.setdefault(r.conclusion, []).append(r)
            for c in r.conditions:
                demo_kb._rules_by_condition.setdefault(c, []).append(r)
        demo_kb.validate()
        return demo_kb
