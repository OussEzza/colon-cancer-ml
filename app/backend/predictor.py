import os
import json
import joblib
import pandas as pd
import time

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
# Lazy-load artifacts (wait for training to finish)
# ==========================================

model = None
scaler = None
selected_genes = None
_artifacts_loaded = False


def _wait_for_files(paths, timeout=300, interval=1):
    """Wait until all paths exist or timeout (seconds)."""
    start = time.time()
    while True:
        if all(os.path.exists(p) for p in paths):
            return True
        if time.time() - start > timeout:
            return False
        time.sleep(interval)


def _load_artifacts(timeout=300):
    """Load model, scaler and selected genes, waiting up to timeout seconds."""
    global model, scaler, selected_genes, _artifacts_loaded

    if _artifacts_loaded:
        return

    paths = [MODEL_PATH, SCALER_PATH, GENES_PATH]

    if not _wait_for_files(paths, timeout=timeout):
        raise FileNotFoundError(
            f"Model artifacts not found in {MODEL_DIR} after {timeout} seconds"
        )

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    with open(GENES_PATH, "r") as f:
        selected_genes = json.load(f)

    _artifacts_loaded = True

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