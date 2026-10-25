"""
Data Preprocessing Pipeline for the Medical Expert System Benchmark.
Cleans raw symptom-disease dataset, standardizes terms, handles missing values,
and prepares benchmark test cases.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

import pandas as pd

from config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    BENCHMARK_DATA_DIR,
    TABLES_DIR,
    PROCESSED_DATA_FILENAME,
    BENCHMARK_DATA_FILENAME,
    KAGGLE_DATASET,
    EXTERNAL_DATASET_SOURCE_URL,
)


def normalize_token(text: Any) -> str:
    """Normalizes symptom or disease name: strips whitespace, lowercases, replaces spaces with underscores."""
    if pd.isna(text) or text is None:
        return ""
    token = str(text).strip().lower()
    token = token.replace(" ", "_").replace("-", "_").replace("/", "_")
    # Clean multiple underscores
    while "__" in token:
        token = token.replace("__", "_")
    return token.strip("_")


class DataPreprocessor:
    """
    Executes full preprocessing pipeline and generates statistical audit reports.
    """

    def __init__(self, raw_data_dir: Path = RAW_DATA_DIR, processed_dir: Path = PROCESSED_DATA_DIR, benchmark_dir: Path = BENCHMARK_DATA_DIR):
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_dir)
        self.benchmark_dir = Path(benchmark_dir)

        self.processed_csv_path = self.processed_dir / PROCESSED_DATA_FILENAME
        self.benchmark_json_path = self.benchmark_dir / BENCHMARK_DATA_FILENAME
        self.report_json_path = TABLES_DIR / "preprocessing_report.json"

    def run_pipeline(self) -> Dict[str, Any]:
        """
        Runs the complete preprocessing workflow and returns summary statistics.
        """
        raw_csv = self.raw_data_dir / "dataset.csv"
        if not raw_csv.exists():
            # Check for any csv
            csvs = list(self.raw_data_dir.glob("*.csv"))
            if not csvs:
                raise FileNotFoundError(f"No CSV dataset found in {self.raw_data_dir}")
            raw_csv = csvs[0]

        # 1. Load Raw Data
        df_raw = pd.read_csv(raw_csv)
        raw_rows, raw_cols = df_raw.shape
        raw_missing = int(df_raw.isna().sum().sum())
        raw_duplicates = int(df_raw.duplicated().sum())

        # 2. Identify Disease and Symptom columns
        disease_col = df_raw.columns[0]
        symptom_cols = list(df_raw.columns[1:])

        # 3. Clean and standardize disease names
        cleaned_records = []
        unique_symptoms_set = set()
        unique_diseases_set = set()

        for idx, row in df_raw.iterrows():
            disease = normalize_token(row[disease_col])
            if not disease:
                continue
            unique_diseases_set.add(disease)

            # Collect valid symptoms for this record
            row_symptoms = []
            for col in symptom_cols:
                val = row[col]
                sym = normalize_token(val)
                if sym and sym not in ["nan", "none", "null"]:
                    row_symptoms.append(sym)
                    unique_symptoms_set.add(sym)

            # Deduplicate symptoms within the same record while preserving order
            seen = set()
            dedup_symptoms = [s for s in row_symptoms if not (s in seen or seen.add(s))]

            if dedup_symptoms:
                cleaned_records.append({
                    "case_id": f"CASE_{idx + 1:05d}",
                    "disease": disease,
                    "symptoms": dedup_symptoms,
                    "symptom_count": len(dedup_symptoms),
                    "symptoms_str": ", ".join(dedup_symptoms),
                })

        # Create processed DataFrame
        df_processed = pd.DataFrame(cleaned_records)
        processed_rows = len(df_processed)

        # 4. Save Processed CSV
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        # Tabular representation for analysis
        df_processed.to_csv(self.processed_csv_path, index=False)

        # 5. Save Benchmark Test Cases JSON
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)
        benchmark_cases = [
            {
                "case_id": r["case_id"],
                "disease": r["disease"],
                "symptoms": r["symptoms"],
            }
            for r in cleaned_records
        ]
        with open(self.benchmark_json_path, "w", encoding="utf-8") as f:
            json.dump(benchmark_cases, f, indent=2)

        # 6. Audit & Preprocessing Report
        report = {
            "source": f"Kaggle: {KAGGLE_DATASET}",
            "external_url": EXTERNAL_DATASET_SOURCE_URL,
            "raw_dataset_file": raw_csv.name,
            "raw_rows": raw_rows,
            "raw_columns": raw_cols,
            "raw_missing_values": raw_missing,
            "raw_duplicate_rows": raw_duplicates,
            "processed_instances": processed_rows,
            "unique_diseases_count": len(unique_diseases_set),
            "unique_symptoms_count": len(unique_symptoms_set),
            "unique_diseases_sample": sorted(list(unique_diseases_set))[:15],
            "unique_symptoms_sample": sorted(list(unique_symptoms_set))[:20],
            "average_symptoms_per_case": round(df_processed["symptom_count"].mean(), 2) if processed_rows > 0 else 0,
            "min_symptoms_per_case": int(df_processed["symptom_count"].min()) if processed_rows > 0 else 0,
            "max_symptoms_per_case": int(df_processed["symptom_count"].max()) if processed_rows > 0 else 0,
            "processed_csv_path": str(self.processed_csv_path),
            "benchmark_json_path": str(self.benchmark_json_path),
        }

        TABLES_DIR.mkdir(parents=True, exist_ok=True)
        with open(self.report_json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report
