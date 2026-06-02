"""
evaluation.py

Evaluate Random Forest wildfire
susceptibility model.

Inputs:
    outputs/models/random_forest.pkl

    data/training/
    ├── X_test.csv
    └── y_test.csv

Outputs:
    outputs/model_evaluation/
    ├── metrics.csv
    ├── classification_report.csv
    ├── cv_scores.csv
    ├── confusion_matrix.png
    └── roc_curve.png
"""

from pathlib import Path
import warnings
import joblib

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

from sklearn.model_selection import (
    cross_val_score
)

warnings.filterwarnings("ignore")

# PATHS

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

OUTPUT_DIR = (
    PROJECT_ROOT /
    "outputs" /
    "model_evaluation"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# FILES

MODEL_PATH = (
    MODEL_DIR /
    "random_forest.pkl"
)

X_TEST_PATH = (
    TRAINING_DIR /
    "X_test.csv"
)

Y_TEST_PATH = (
    TRAINING_DIR /
    "y_test.csv"
)


# LOAD MODEL

print("\nLoading model")

model = joblib.load(
    MODEL_PATH
)

print(
    "Model loaded"
)


# LOAD TEST DATA

print("\nLoading test data")

X_test = pd.read_csv(
    X_TEST_PATH
)

y_test = pd.read_csv(
    Y_TEST_PATH
).squeeze()

print(
    f"Testing samples: {len(X_test):,}"
)

# PREDICTIONS

print("\nGenerating predictions")

y_pred = model.predict(
    X_test
)

y_prob = model.predict_proba(
    X_test
)[:, 1]


# STANDARD METRICS

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred
)

recall = recall_score(
    y_test,
    y_pred
)

f1 = f1_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

# 5-FOLD CROSS VALIDATION

print("\nRunning 5-Fold Cross Validation")

cv_scores = cross_val_score(

    estimator=model,

    X=X_test,

    y=y_test,

    cv=5,

    scoring="roc_auc",

    n_jobs=-1

)

cv_mean = cv_scores.mean()

cv_std = cv_scores.std()


# SAVE CV SCORES

cv_df = pd.DataFrame({

    "Fold": [
        1,
        2,
        3,
        4,
        5
    ],

    "ROC_AUC": cv_scores

})

cv_df.to_csv(

    OUTPUT_DIR /
    "cv_scores.csv",

    index=False

)


# SAVE METRICS

metrics_df = pd.DataFrame({

    "Metric": [

        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC AUC",
        "CV ROC AUC Mean",
        "CV ROC AUC Std"

    ],

    "Value": [

        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        cv_mean,
        cv_std

    ]

})

metrics_df.to_csv(

    OUTPUT_DIR /
    "metrics.csv",

    index=False

)

# CLASSIFICATION REPORT

report = classification_report(

    y_test,
    y_pred,

    output_dict=True

)

report_df = pd.DataFrame(
    report
).transpose()

report_df.to_csv(

    OUTPUT_DIR /
    "classification_report.csv"

)


# CONFUSION MATRIX

print("\nCreating confusion matrix")

cm = confusion_matrix(
    y_test,
    y_pred
)

fig, ax = plt.subplots(
    figsize=(6, 6)
)

ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=[
        "Unburned",
        "Burned"
    ]

).plot(
    ax=ax
)

plt.title(
    "Confusion Matrix"
)

plt.savefig(

    OUTPUT_DIR /
    "confusion_matrix.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()


# ROC CURVE

print("\nCreating ROC Curve")

fig, ax = plt.subplots(
    figsize=(6, 6)
)

RocCurveDisplay.from_predictions(

    y_test,

    y_prob,

    ax=ax

)

plt.title(
    "ROC Curve"
)

plt.savefig(

    OUTPUT_DIR /
    "roc_curve.png",

    dpi=300,

    bbox_inches="tight"

)

plt.close()

# SUMMARY

print("\n===================================")
print("MODEL EVALUATION COMPLETE")
print("===================================")

print(
    f"Accuracy        : {accuracy:.4f}"
)

print(
    f"Precision       : {precision:.4f}"
)

print(
    f"Recall          : {recall:.4f}"
)

print(
    f"F1 Score        : {f1:.4f}"
)

print(
    f"ROC AUC         : {roc_auc:.4f}"
)

print(
    f"CV ROC AUC Mean : {cv_mean:.4f}"
)

print(
    f"CV ROC AUC Std  : {cv_std:.4f}"
)

print(
    f"\nResults saved to:\n{OUTPUT_DIR}"
)