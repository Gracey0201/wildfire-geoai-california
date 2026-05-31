"""
feature_importance.py

Calculate Random Forest
feature importance.

Input:
    outputs/models/random_forest.pkl

Output:
    outputs/feature_importance/
    ├── feature_importance.csv
    └── feature_importance.png
"""

from pathlib import Path
import warnings
import joblib

import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path.cwd()

MODEL_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "models"
)

OUTPUT_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "feature_importance"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# FILES
# =========================================================

MODEL_PATH = (
    MODEL_DIR /
    "random_forest.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading model")

model = joblib.load(
    MODEL_PATH
)

print(
    "Model loaded"
)


# =========================================================
# FEATURE NAMES
# =========================================================

feature_names = [

    "dem",

    "slope",

    "twi",

    "precipitation",

    "landcover",

    "distance_to_roads",

    "distance_to_settlements"

]


# =========================================================
# EXTRACT IMPORTANCE
# =========================================================

importance_df = pd.DataFrame({

    "Feature":
        feature_names,

    "Importance":
        model.feature_importances_

})

importance_df = importance_df.sort_values(

    by="Importance",

    ascending=False

)


# =========================================================
# SAVE CSV
# =========================================================

importance_df.to_csv(

    OUTPUT_DIR /
    "feature_importance.csv",

    index=False

)

print(
    "\nFeature importance table saved"
)


# =========================================================
# CREATE FIGURE
# =========================================================

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.barh(

    importance_df["Feature"],

    importance_df["Importance"]

)

ax.set_xlabel(
    "Importance"
)

ax.set_ylabel(
    "Predictor"
)

ax.set_title(
    "Random Forest Feature Importance"
)

ax.invert_yaxis()

plt.tight_layout()

plt.savefig(

    OUTPUT_DIR /
    "feature_importance.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# =========================================================
# PRINT RESULTS
# =========================================================

print("\n===================================")
print("FEATURE IMPORTANCE COMPLETE")
print("===================================\n")

print(
    importance_df.to_string(
        index=False
    )
)

print(
    f"\nResults saved to:\n{OUTPUT_DIR}"
)