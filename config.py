"""
Configuration module for the Explainable Medical Expert System.
Course: ECSCT24301 - Foundation of AI, Adani University.
Applied AI Project Track.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BENCHMARK_DATA_DIR = DATA_DIR / "benchmark"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
TABLES_DIR = OUTPUTS_DIR / "tables"
BENCHMARK_RESULTS_DIR = OUTPUTS_DIR / "benchmark_results"

DOCS_DIR = PROJECT_ROOT / "docs"

# Ensure runtime directories exist
for directory in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    BENCHMARK_DATA_DIR,
    KNOWLEDGE_BASE_DIR,
    CHARTS_DIR,
    TABLES_DIR,
    BENCHMARK_RESULTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset Configuration
# Standard open-access benchmark dataset for disease-symptom evaluation
KAGGLE_DATASET = "itachi9604/disease-symptom-description-dataset"
EXTERNAL_DATASET_SOURCE_URL = "https://data.mendeley.com/datasets/2cxccsxydc/1"
RAW_DATA_FILENAME = "dataset.csv"
PROCESSED_DATA_FILENAME = "processed_symptom_disease.csv"
BENCHMARK_DATA_FILENAME = "benchmark_cases.json"

# Knowledge Base Files
RULES_CSV_PATH = KNOWLEDGE_BASE_DIR / "medical_rules.csv"
RULES_JSON_PATH = KNOWLEDGE_BASE_DIR / "medical_rules.json"

# Academic & Institutional Metadata
UNIVERSITY_NAME = "Adani University"
FACULTY_NAME = "Faculty of Engineering Sciences and Technology (FEST)"
DEPARTMENT_NAME = "Computer Science and Engineering (AI-ML)"
COURSE_CODE = "ECSCT24301"
COURSE_NAME = "Foundation of AI"
PROJECT_TRACK = "Applied AI Project Track"
PROJECT_TITLE = "Explainable Medical Expert System Using Rule-Based AI with Forward and Backward Chaining"
APP_SHORT_TITLE = "Explainable Medical Expert System"

TEAM_MEMBERS = [
    {"name": "Jeel Parikh", "usn": "2410111080", "role": "AI Reasoning & Forward/Backward Chaining"},
    {"name": "Krish Patel", "usn": "2410111102", "role": "Knowledge Engineering & Benchmarking"},
    {"name": "Chintan Patel", "usn": "2410111090", "role": "Data Preprocessing & UI Architecture"},
]

# Educational Medical Disclaimer - Mandatory throughout application
DISCLAIMER_SHORT = "Educational AI Prototype – Not a Medical Diagnostic Tool"
DISCLAIMER_FULL = (
    "Educational AI Prototype – Not a Medical Diagnostic Tool. "
    "This system is an academic demonstration of classical rule-based AI reasoning "
    "(Forward Chaining, Backward Chaining, and Rule Prioritization) for course ECSCT24301. "
    "It does NOT provide clinical diagnoses, treatments, or prescriptions. "
    "In any real-life health situation, consult a licensed healthcare professional."
)

# Prioritized Forward Chaining Default Hyperparameters
DEFAULT_ALPHA = 0.40   # Specificity weight
DEFAULT_BETA = 0.35    # Evidence weight
DEFAULT_GAMMA = 0.25   # Relevance weight

# Inference Safety Limits
MAX_INFERENCE_ITERATIONS = 100
MAX_BACKWARD_DEPTH = 15

# Benchmark Presets
BENCHMARK_CASE_PRESETS = [10, 50, 100, 500, 1000]
KB_SIZE_PRESETS = [25, 50, 100, 250, 500]
