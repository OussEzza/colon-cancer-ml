import os
import json
import joblib
import pandas as pd

# ==========================================
# Paths
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = "/model"

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

GENES_PATH = os.path.join(
    MODEL_DIR,
    "selected_genes.json"
)

# ==========================================
# Load artifacts
# ==========================================

model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)

with open(GENES_PATH, "r") as f:
    selected_genes = json.load(f)

# ==========================================
# Prediction function
# ==========================================

def predict(input_data: dict):

    ordered_values = [
        input_data[gene]
        for gene in selected_genes
    ]

    df = pd.DataFrame(
        [ordered_values],
        columns=selected_genes
    )

    scaled_data = scaler.transform(df)

    prediction = model.predict(scaled_data)[0]

    probabilities = model.predict_proba(
        scaled_data
    )[0]

    confidence = float(max(probabilities))

    label = (
        "Abnormal"
        if prediction == 1
        else "Normal"
    )

    return {
        "prediction": label,
        "confidence": round(confidence, 4)
    }