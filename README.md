# 🧬 Colon Cancer Prediction - Machine Learning Application

A machine learning web application for predicting colon cancer based on gene expression analysis using FastAPI backend and modern HTML/CSS/JavaScript frontend.

## 📋 Project Overview

This project implements an intelligent cancer prediction system that analyzes gene expression values and predicts the likelihood of colon cancer. It features:

- **Backend API**: FastAPI-based REST API for predictions
- **Frontend UI**: Modern, responsive web interface with demo data
- **Docker Support**: Complete containerization for easy deployment
- **ML Model**: Trained model using selected gene biomarkers
- **Demo Data**: Pre-filled test cases (normal and abnormal samples)

## 📁 Project Structure

```
colon-cancer-ml/
├── app/
│   ├── Dockerfile                 # Docker image for backend
│   ├── requirements.txt           # Python dependencies
│   ├── backend/
│   │   ├── main.py               # FastAPI application
│   │   ├── predictor.py          # ML prediction logic
│   │   └── __pycache__/
│   └── frontend/
│       ├── index.html            # Web interface
│       ├── script.js             # Frontend logic
│       └── style.css             # Styling
├── training/
│   ├── Dockerfile               # Docker image for training
│   ├── requirements.txt         # Training dependencies
│   ├── train.py                 # Model training script
│   └── data/
│       └── colon_cancer_dataset.csv
├── model/
│   └── selected_genes.json      # Gene identifiers for prediction
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed on your system
- Or **Python 3.11+** with pip (for local development)

### Installation & Running

#### Option 1: Using Docker Compose (Recommended)

1. **Clone or download the project**
   ```bash
   cd colon-cancer-ml
   ```

2. **Build and run with Docker Compose**
   ```bash
   sudo docker compose up --build
   ```

   This command will:
   - Build the backend and training Docker images
   - Install all dependencies
   - Start the FastAPI server
   - Serve the frontend application

3. **Access the application**
   - Open your browser and navigate to: `http://localhost:8000`
   - The frontend will load automatically

4. **Stopping the application**
   ```bash
   sudo docker compose down
   ```

#### Option 2: Local Development Setup

1. **Install Python 3.11+**

2. **Install backend dependencies**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Access the application**
   - Open your browser to: `http://localhost:8000`

## 🎯 How to Use the Application

1. **Enter Gene Expression Values**
   - Input normalized gene expression values for the 6 analyzed genes (M63391, T62947, D14812, T51250, H66976, X55362)


2. **Get Prediction**
   - Click **🧬 Predict** to analyze the gene expression
   - View the result showing:
     - Prediction: Positive (Cancer Detected) or Negative (Healthy)
     - Confidence Score: Prediction certainty percentage

3. **Clear Form**
   - Click **🗑️ Clear** to reset all inputs

## 🔧 API Endpoints

### `GET /`
Returns the frontend HTML index page

### `GET /genes`
Returns the list of selected genes for prediction
```json
{
  "selected_genes": ["M63391", "T62947", "D14812", "T51250", "H66976", "X55362"]
}
```

### `POST /predict`
Predicts cancer based on gene expression values

**Request Body:**
```json
{
  "M63391": 1024.5,
  "T62947": 892.3,
  "D14812": 756.8,
  "T51250": 1205.1,
  "H66976": 567.4,
  "X55362": 934.7
}
```

**Response:**
```json
{
  "prediction": "Positive",
  "confidence": 0.85
}
```

### `GET /health`
Health check endpoint
```json
{
  "status": "healthy"
}
```

## 📦 Dependencies

### Backend (app/requirements.txt)
- fastapi: Web framework
- uvicorn: ASGI server
- scikit-learn: ML model and data processing
- pandas: Data manipulation
- numpy: Numerical computing

### Training (training/requirements.txt)
- scikit-learn: ML algorithms
- pandas: Data processing
- numpy: Numerical operations

## 🧪 Demo Data

### Normal Sample (Healthy)
- Simulates healthy gene expression with lower values
- Expected: **Negative** (No Cancer)

### Abnormal Sample (Cancer)
- Simulates elevated gene expression typical in cancer
- Expected: **Positive** (Cancer Detected)

## 🏗️ Architecture

### Backend Flow
1. Frontend sends POST request with gene expression values
2. FastAPI endpoint receives and validates data
3. Predictor loads trained ML model
4. Model processes gene expression values
5. Returns prediction and confidence score
6. Frontend displays results with visual indicators

### Frontend Flow
1. Load available genes from API
2. Generate dynamic input fields
3. Handle form submission
4. Display prediction results
5. Support demo data loading and form clearing

## 📊 Model Information

The prediction model is trained using selected gene biomarkers that are strong indicators of colon cancer. The model uses:
- **Algorithm**: Classification model (e.g., SVM, Random Forest, or Logistic Regression)
- **Selected Genes**: 6 gene expression markers
- **Input**: Normalized gene expression values
- **Output**: Binary classification (Positive/Negative) with confidence score

## 🐛 Troubleshooting

### Docker Build Fails
```bash
# Clean up and rebuild
sudo docker compose down -v
sudo docker compose up --build
```

### Port 8000 Already in Use
```bash
# Change the port in docker-compose.yml or kill the process
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Connection Refused Error
- Ensure Docker containers are running: `docker compose ps`
- Wait a few seconds for services to start
- Check Docker logs: `docker compose logs -f`

### API Not Responding
```bash
# Check API health
curl http://localhost:8000/health
```

## 📝 Development Notes

- The model should be pre-trained and located at `model/` directory
- Gene selection is defined in `model/selected_genes.json`
- CORS is enabled for all origins (configure in production)
- Frontend loads genes dynamically from the API

## 🔒 Production Considerations

- Remove `allow_origins=["*"]` from CORS middleware
- Add authentication and authorization
- Implement rate limiting
- Add input validation and sanitization
- Use environment variables for configuration
- Consider adding logging and monitoring
- Deploy with a production-grade web server (Gunicorn, Nginx)

## 📄 License

This project is part of the Methodologie course at [Institution Name].

## 👤 Author

Created for educational purposes in Machine Learning and Web Development.

---

**Last Updated**: May 19, 2026

For questions or issues, please refer to the project documentation or contact the development team.
