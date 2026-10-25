#!/usr/bin/env python3
"""
CLI Script to execute preprocessing on raw dataset.
Usage: python scripts/preprocess_dataset.py
"""

import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import DataPreprocessor


def main():
    print("=" * 60)
    print("Medical Expert System - Data Preprocessing Pipeline")
    print("=" * 60)

    preprocessor = DataPreprocessor()
    print("Running normalization, missing-value handling, and case generation...")

    report = preprocessor.run_pipeline()

    print("\n[PREPROCESSING REPORT]")
    print(f"Data Source:               {report.get('source')}")
    print(f"Raw Records:               {report.get('raw_rows')}")
    print(f"Raw Columns:               {report.get('raw_columns')}")
    print(f"Missing Values Cleaned:    {report.get('raw_missing_values')}")
    print(f"Duplicate Rows Handled:    {report.get('raw_duplicate_rows')}")
    print(f"Processed Instances:       {report.get('processed_instances')}")
    print(f"Unique Diseases:           {report.get('unique_diseases_count')}")
    print(f"Unique Symptoms:           {report.get('unique_symptoms_count')}")
    print(f"Average Symptoms / Case:   {report.get('average_symptoms_per_case')}")
    print(f"Output Processed CSV:      {report.get('processed_csv_path')}")
    print(f"Output Benchmark JSON:     {report.get('benchmark_json_path')}")
    print("=" * 60)
    print("Preprocessing completed successfully!")


if __name__ == "__main__":
    main()
