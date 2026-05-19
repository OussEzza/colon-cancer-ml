import os
import json
import joblib
import warnings

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

warnings.filterwarnings("ignore")

# ==========================================
# Paths
# ==========================================

DATA_PATH = "data/colon_cancer_dataset.csv"
MODEL_DIR = "/model"

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================
# Load dataset
# ==========================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

X_raw = df.drop("Class", axis=1)

y_raw = LabelEncoder().fit_transform(
    df["Class"]
)

feature_names = X_raw.columns.tolist()

# ==========================================
# Scale FULL dataset
# ==========================================

scaler_full = StandardScaler()

X_scaled_full = scaler_full.fit_transform(
    X_raw
)

# ==========================================
# Forward Feature Selection
# ==========================================

SELECTION_STEPS = 10

available_features = list(
    range(X_scaled_full.shape[1])
)

selected_indices = []

selected_names = []

global_accuracies = []

print("\n===================================")
print("GLOBAL GENE SELECTION")
print("===================================\n")

for step in range(SELECTION_STEPS):

    best_acc = 0.0

    best_idx = None

    for idx in available_features:

        temp_indices = (
            selected_indices + [idx]
        )

        model = LogisticRegression(
            random_state=42
        )

        model.fit(
            X_scaled_full[:, temp_indices],
            y_raw
        )

        predictions = model.predict(
            X_scaled_full[:, temp_indices]
        )

        acc = accuracy_score(
            y_raw,
            predictions
        )

        if acc > best_acc:

            best_acc = acc

            best_idx = idx

    selected_indices.append(best_idx)

    selected_names.append(
        feature_names[best_idx]
    )

    global_accuracies.append(best_acc)

    available_features.remove(best_idx)

    print(
        f"Step {step+1}: "
        f"{feature_names[best_idx]} "
        f"-> {best_acc*100:.2f}%"
    )

# ==========================================
# Display selected genes
# ==========================================

print("\n===================================")
print("TOP 10 SELECTED GENES")
print("===================================\n")

for i, gene in enumerate(selected_names):

    print(f"{i+1}. {gene}")

# ==========================================
# FINAL MODEL USING TOP 6 GENES
# ==========================================

FINAL_GENE_COUNT = 6

final_genes = selected_names[:FINAL_GENE_COUNT]

print("\n===================================")
print("FINAL GENES USED FOR MODEL")
print("===================================\n")

for gene in final_genes:
    print(gene)

# ==========================================
# Build final dataset
# ==========================================

X_final = df[final_genes]

y = y_raw

# ==========================================
# Train/Test split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_final,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# Scaling
# ==========================================

final_scaler = StandardScaler()

X_train_scaled = final_scaler.fit_transform(
    X_train
)

X_test_scaled = final_scaler.transform(
    X_test
)

# ==========================================
# Final model
# ==========================================

final_model = LogisticRegression(
    random_state=42
)

print("\nTraining final model...\n")

final_model.fit(
    X_train_scaled,
    y_train
)

# ==========================================
# Evaluation
# ==========================================

train_predictions = final_model.predict(
    X_train_scaled
)

test_predictions = final_model.predict(
    X_test_scaled
)

train_acc = accuracy_score(
    y_train,
    train_predictions
)

test_acc = accuracy_score(
    y_test,
    test_predictions
)

print("\n===================================")
print("FINAL MODEL RESULTS")
print("===================================\n")

print(
    f"Training Accuracy: "
    f"{train_acc*100:.2f}%"
)

print(
    f"Testing Accuracy: "
    f"{test_acc*100:.2f}%"
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        test_predictions
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        test_predictions
    )
)

# ==========================================
# Save artifacts
# ==========================================

print("\nSaving artifacts...\n")

joblib.dump(
    final_model,
    os.path.join(
        MODEL_DIR,
        "model.pkl"
    )
)

joblib.dump(
    final_scaler,
    os.path.join(
        MODEL_DIR,
        "scaler.pkl"
    )
)

# Save ONLY final 6 genes
with open(
    os.path.join(
        MODEL_DIR,
        "selected_genes.json"
    ),
    "w"
) as f:

    json.dump(
        final_genes,
        f,
        indent=4
    )

print("Artifacts saved successfully.")

print("\nDONE.")