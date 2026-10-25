#!/usr/bin/env python3
"""
CLI Script to execute empirical benchmark runs.
Usage: python scripts/run_benchmark.py [--cases 50] [--kb-size 39]
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.benchmark import BenchmarkEngine


def main():
    parser = argparse.ArgumentParser(description="Run Empirical Benchmark for Medical Expert System")
    parser.add_argument("--cases", type=int, default=50, help="Number of test cases (default: 50)")
    parser.add_argument("--kb-size", type=int, default=None, help="Knowledge base size in rules (default: full KB)")
    args = parser.parse_args()

    print("=" * 65)
    print("Medical Expert System - Empirical Benchmark Execution")
    print(f"Test Cases: {args.cases} | KB Size: {args.kb_size or 'Default'}")
    print("=" * 65)

    benchmarker = BenchmarkEngine()
    results = benchmarker.run_benchmark(test_case_count=args.cases, kb_size=args.kb_size)

    print("\n[BENCHMARK SUMMARY RESULTS]")
    print(results["summary_df"].to_string(index=False))
    print("-" * 65)
    print(f"Total Benchmark Time: {results['total_time_ms']:.2f} ms")
    print(f"Summary CSV:  {results['summary_csv_path']}")
    print(f"Detailed CSV: {results['detailed_csv_path']}")
    print(f"JSON Export:  {results['json_path']}")
    print("=" * 65)


if __name__ == "__main__":
    main()
