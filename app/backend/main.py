from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend.predictor import (
    predict,
    selected_genes
)

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

    return {
        "selected_genes": selected_genes
    }


@app.post("/predict")
def predict_endpoint(
    input_data: dict
):

    # Check all genes exist
    for gene in selected_genes:

        if gene not in input_data:

            return {
                "error": (
                    f"Missing gene: {gene}"
                )
            }

    result = predict(input_data)

    return result