"""
random_forest.py

Train a Random Forest wildfire
susceptibility model.

Input:
    data/training/training_data.csv

Outputs:
    outputs/models/random_forest.pkl

    data/training/
    ├── X_train.csv
    ├── X_test.csv
    ├── y_train.csv
    └── y_test.csv
"""

from pathlib import Path
import warnings
import joblib

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")


# =========================================================
# SETTINGS
# =========================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

N_ESTIMATORS = 500


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path.cwd()

TRAINING_DIR = (
    PROJECT_ROOT /
    "data" /
    "training"
)

MODEL_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INPUT_CSV = (
    TRAINING_DIR /
    "training_data.csv"
)

MODEL_PATH = (
    MODEL_DIR /
    "random_forest.pkl"
)


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading training data")

df = pd.read_csv(
    INPUT_CSV
)

print(
    f"Samples: {len(df):,}"
)

print(
    f"Columns: {list(df.columns)}"
)


# =========================================================
# FEATURES / LABELS
# =========================================================

X = df.drop(
    columns=[
        "label"
    ]
)

y = df[
    "label"
]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

print("\nCreating train/test split")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y

)

print(
    f"Training samples: {len(X_train):,}"
)

print(
    f"Testing samples: {len(X_test):,}"
)


# =========================================================
# SAVE SPLITS
# =========================================================

X_train.to_csv(
    TRAINING_DIR /
    "X_train.csv",
    index=False
)

X_test.to_csv(
    TRAINING_DIR /
    "X_test.csv",
    index=False
)

y_train.to_csv(
    TRAINING_DIR /
    "y_train.csv",
    index=False
)

y_test.to_csv(
    TRAINING_DIR /
    "y_test.csv",
    index=False
)

print(
    "\nTrain/test datasets saved"
)


# =========================================================
# TRAIN MODEL
# =========================================================

print("\nTraining Random Forest")

rf = RandomForestClassifier(

    n_estimators=N_ESTIMATORS,

    random_state=RANDOM_STATE,

    n_jobs=-1

)

rf.fit(
    X_train,
    y_train
)

print(
    "Training complete"
)


# =========================================================
# SAVE MODEL
# =========================================================

joblib.dump(
    rf,
    MODEL_PATH
)

print(
    f"\nModel saved:\n{MODEL_PATH}"
)


# =========================================================
# SUMMARY
# =========================================================

print("\n===================================")
print("RANDOM FOREST COMPLETE")
print("===================================")

print(
    f"Trees: {N_ESTIMATORS}"
)

print(
    f"Training samples: {len(X_train):,}"
)

print(
    f"Testing samples: {len(X_test):,}"
)