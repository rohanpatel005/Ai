"""
Knowledge Base Management and Validation Module.
Handles rule loading, validation, indexing, querying, and format synchronization.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set

import pandas as pd

from config import (
    KNOWLEDGE_BASE_DIR,
    RULES_CSV_PATH,
    RULES_JSON_PATH,
)
from src.models import Rule


class KnowledgeBaseValidationResult:
    """Stores the outcome of knowledge base rule integrity checks."""

    def __init__(self):
        self.is_valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.rule_count: int = 0
        self.unique_conditions_count: int = 0
        self.unique_conclusions_count: int = 0


class KnowledgeBase:
    """
    In-memory knowledge base of explicit IF-THEN rules with indexing and validation.
    """

    def __init__(self, json_path: Optional[Path] = None, csv_path: Optional[Path] = None):
        self.json_path = Path(json_path) if json_path else RULES_JSON_PATH
        self.csv_path = Path(csv_path) if csv_path else RULES_CSV_PATH
        self.rules: List[Rule] = []
        self._rules_by_id: Dict[str, Rule] = {}
        self._rules_by_conclusion: Dict[str, List[Rule]] = {}
        self._rules_by_condition: Dict[str, List[Rule]] = {}
        self.validation_result: Optional[KnowledgeBaseValidationResult] = None

        self.load_rules()

    def load_rules(self) -> List[Rule]:
        """Loads rules from JSON (preferred) or CSV fallback, building lookup indexes."""
        self.rules = []
        self._rules_by_id = {}
        self._rules_by_conclusion = {}
        self._rules_by_condition = {}

        if self.json_path.exists():
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    rule = Rule.from_dict(item)
                    self.rules.append(rule)
        elif self.csv_path.exists():
            df = pd.read_csv(self.csv_path)
            for _, row in df.iterrows():
                rule = Rule.from_dict(row.to_dict())
                self.rules.append(rule)

        # Build indexing
        for rule in self.rules:
            self._rules_by_id[rule.rule_id] = rule
            self._rules_by_conclusion.setdefault(rule.conclusion, []).append(rule)
            for cond in rule.conditions:
                self._rules_by_condition.setdefault(cond, []).append(rule)

        # Validate on load
        self.validate()
        return self.rules

    def validate(self) -> KnowledgeBaseValidationResult:
        """
        Validates all rules according to formal integrity constraints:
        - Rule ID exists, non-empty, unique
        - Conditions non-empty list of valid strings
        - Conclusion exists and non-empty
        - Evidence weight is numeric in [0.0, 1.0]
        - Priority is numeric in [0.0, 1.0]
        - Specificity is positive integer
        - Source citation exists
        """
        result = KnowledgeBaseValidationResult()
        seen_ids: Set[str] = set()
        conditions_set: Set[str] = set()
        conclusions_set: Set[str] = set()

        if not self.rules:
            result.is_valid = False
            result.errors.append("Knowledge base is empty; no rules loaded.")
            self.validation_result = result
            return result

        for idx, rule in enumerate(self.rules):
            prefix = f"Rule #{idx + 1} ({rule.rule_id or 'NO_ID'}): "

            # 1. Rule ID validation
            if not rule.rule_id:
                result.errors.append(f"{prefix}Missing rule_id.")
                result.is_valid = False
            elif rule.rule_id in seen_ids:
                result.errors.append(f"{prefix}Duplicate rule_id '{rule.rule_id}'.")
                result.is_valid = False
            else:
                seen_ids.add(rule.rule_id)

            # 2. Conditions validation
            if not rule.conditions or not isinstance(rule.conditions, list):
                result.errors.append(f"{prefix}Conditions must be a non-empty list.")
                result.is_valid = False
            else:
                for cond in rule.conditions:
                    if not cond or not isinstance(cond, str) or not cond.strip():
                        result.errors.append(f"{prefix}Contains empty condition token.")
                        result.is_valid = False
                    else:
                        conditions_set.add(cond.strip().lower())

            # 3. Conclusion validation
            if not rule.conclusion or not isinstance(rule.conclusion, str) or not rule.conclusion.strip():
                result.errors.append(f"{prefix}Missing conclusion.")
                result.is_valid = False
            else:
                conclusions_set.add(rule.conclusion.strip().lower())

            # 4. Evidence weight validation
            if not (0.0 <= rule.evidence_weight <= 1.0):
                result.errors.append(f"{prefix}Evidence weight {rule.evidence_weight} must be between 0.0 and 1.0.")
                result.is_valid = False

            # 5. Priority validation
            if not (0.0 <= rule.priority <= 1.0):
                result.errors.append(f"{prefix}Priority {rule.priority} must be between 0.0 and 1.0.")
                result.is_valid = False

            # 6. Specificity validation
            if rule.specificity < 1:
                result.warnings.append(f"{prefix}Specificity is {rule.specificity}; should typically be >= 1.")

            # 7. Source validation
            if not rule.source or not rule.source.strip():
                result.warnings.append(f"{prefix}Source citation is missing.")

        result.rule_count = len(self.rules)
        result.unique_conditions_count = len(conditions_set)
        result.unique_conclusions_count = len(conclusions_set)

        self.validation_result = result
        return result

    def get_all_rules(self) -> List[Rule]:
        return list(self.rules)

    def get_rule_by_id(self, rule_id: str) -> Optional[Rule]:
        return self._rules_by_id.get(rule_id)

    def get_rules_by_conclusion(self, conclusion: str) -> List[Rule]:
        return self._rules_by_conclusion.get(conclusion.strip().lower(), [])

    def get_rules_by_condition(self, condition: str) -> List[Rule]:
        return self._rules_by_condition.get(condition.strip().lower(), [])

    def get_all_conclusions(self) -> List[str]:
        return sorted(list(self._rules_by_conclusion.keys()))

    def get_all_conditions(self) -> List[str]:
        return sorted(list(self._rules_by_condition.keys()))

    def save_rules(self) -> None:
        """Persists current in-memory rules to both JSON and CSV files."""
        self.json_path.parent.mkdir(parents=True, exist_ok=True)

        # Save JSON
        dict_rules = [r.to_dict() for r in self.rules]
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(dict_rules, f, indent=2)

        # Save CSV
        csv_rows = []
        for r in self.rules:
            row = r.to_dict()
            row["conditions"] = ", ".join(r.conditions)
            csv_rows.append(row)
        df = pd.DataFrame(csv_rows)
        df.to_csv(self.csv_path, index=False)

    def create_subset(self, size: int) -> "KnowledgeBase":
        """Returns a new KnowledgeBase containing a subset of the rules for scalability testing."""
        subset_kb = KnowledgeBase.__new__(KnowledgeBase)
        subset_kb.json_path = self.json_path
        subset_kb.csv_path = self.csv_path
        subset_kb.rules = list(self.rules[:size])
        subset_kb._rules_by_id = {r.rule_id: r for r in subset_kb.rules}
        subset_kb._rules_by_conclusion = {}
        subset_kb._rules_by_condition = {}
        for r in subset_kb.rules:
            subset_kb._rules_by_conclusion.setdefault(r.conclusion, []).append(r)
            for c in r.conditions:
                subset_kb._rules_by_condition.setdefault(c, []).append(r)
        subset_kb.validate()
        return subset_kb
