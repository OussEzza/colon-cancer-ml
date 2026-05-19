from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend import predictor

app = FastAPI(
    title="Colon Cancer Prediction API"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

# ==========================================
# Routes
# ==========================================

@app.get("/")
def home():

    return FileResponse(
        os.path.join(
            FRONTEND_DIR,
            "index.html"
        )
    )

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/genes")
def genes():

    # Ensure artifacts are loaded and return the selected genes
    try:
        predictor._load_artifacts()
    except FileNotFoundError:
        return {"selected_genes": []}

    return {"selected_genes": predictor.selected_genes}


@app.post("/predict")
def predict_endpoint(
    input_data: dict
):

    # Ensure artifacts are loaded before validation and prediction
    try:
        predictor._load_artifacts()
    except FileNotFoundError:
        return {"error": "Model artifacts not available yet"}

    # Check all genes exist
    for gene in predictor.selected_genes:
        if gene not in input_data:
            return {"error": f"Missing gene: {gene}"}

    result = predictor.predict(input_data)

    return result