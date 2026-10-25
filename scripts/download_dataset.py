#!/usr/bin/env python3
"""
CLI Script to download the external benchmark dataset.
Usage: python scripts/download_dataset.py [--force]
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.kaggle_downloader import KaggleDownloader


def main():
    parser = argparse.ArgumentParser(description="Download external benchmark dataset for Medical Expert System")
    parser.add_argument("--force", action="store_true", help="Force redownload even if dataset exists locally")
    args = parser.parse_args()

    print("=" * 60)
    print("Medical Expert System - External Dataset Downloader")
    print("=" * 60)

    downloader = KaggleDownloader()
    print(f"Target directory: {downloader.target_dir}")
    print(f"Configured dataset: {downloader.dataset_name}")

    if downloader.is_dataset_available_locally() and not args.force:
        path = downloader.get_local_dataset_path()
        print(f"[STATUS] Local dataset detected at: {path}")
        print("Skipping download (use --force to override).")
        return

    print("Attempting automatic download via kagglehub...")
    result = downloader.download(force=args.force)

    if result.get("success"):
        print(f"[SUCCESS] {result.get('message')}")
        print(f"Dataset path: {result.get('path')}")
    else:
        print(f"[WARNING] {result.get('message')}")
        print("\nFallback: Generating verified local benchmark dataset to ensure offline functionality...")
        local_path = downloader.generate_bundled_benchmark_dataset()
        print(f"[READY] Bundled benchmark dataset generated at: {local_path}")
        print("\nSetup instructions for future Kaggle API synchronization:")
        print(result.get("instructions", "See README for Kaggle API setup."))


if __name__ == "__main__":
    main()
