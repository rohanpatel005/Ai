"""
Data loader utilities for loading raw, processed, and benchmark datasets.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd

from config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    BENCHMARK_DATA_DIR,
    TABLES_DIR,
    PROCESSED_DATA_FILENAME,
    BENCHMARK_DATA_FILENAME,
)


class DataLoader:
    """Provides safe loading and caching of processed dataset and benchmark cases."""

    @staticmethod
    def get_preprocessing_report() -> Optional[Dict[str, Any]]:
        report_file = TABLES_DIR / "preprocessing_report.json"
        if report_file.exists():
            with open(report_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    @staticmethod
    def load_processed_data() -> Optional[pd.DataFrame]:
        processed_csv = PROCESSED_DATA_DIR / PROCESSED_DATA_FILENAME
        if processed_csv.exists():
            return pd.read_csv(processed_csv)
        return None

    @staticmethod
    def load_benchmark_cases(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        benchmark_json = BENCHMARK_DATA_DIR / BENCHMARK_DATA_FILENAME
        if not benchmark_json.exists():
            return []
        with open(benchmark_json, "r", encoding="utf-8") as f:
            cases = json.load(f)
        if limit is not None and limit > 0:
            return cases[:limit]
        return cases

    @staticmethod
    def get_all_symptoms() -> List[str]:
        """Returns sorted list of all unique symptoms found in processed dataset or returns fallback list."""
        df = DataLoader.load_processed_data()
        if df is not None and not df.empty:
            symptoms_set = set()
            for s_str in df["symptoms_str"].dropna():
                for s in s_str.split(","):
                    clean = s.strip()
                    if clean:
                        symptoms_set.add(clean)
            return sorted(list(symptoms_set))
        return []
