# 🧠 Sentiment Intelligence System

> **Experiment 3 - Lab Practice II** | MTech 2026  
> LSTM-based Sentiment Analysis System with MLOps Best Practices

---

## 📋 Project Overview

A comprehensive sentiment analysis system that classifies product/movie reviews as **Positive** or **Negative** using a **Bidirectional LSTM** deep learning model. The system includes:

- **Deep Learning Model**: Bidirectional LSTM trained on 50,000 IMDB reviews
- **Interactive Dashboard**: Real-time sentiment visualization with charts & analytics
- **REST API**: FastAPI-based inference service with monitoring
- **MLOps Pipeline**: MLflow experiment tracking, model versioning, and reproducible experiments

---

## 🏗️ Architecture

```
Sentiment-Intelligence-System/
├── data/
│   └── IMDB Dataset.csv           # Training dataset (50K reviews)
├── models/
│   ├── sentiment_lstm_model.h5    # Trained LSTM model
│   └── tokenizer.pkl             # Fitted tokenizer
├── notebooks/
│   └── sentiment_training.ipynb   # Jupyter training notebook
├── api/
│   ├── app.py                    # FastAPI REST API
│   └── predictions_log.csv       # Prediction history
├── dashboard/
│   └── index.html                # Interactive visualization dashboard
├── reports/
│   ├── sentiment_distribution.png
│   ├── review_length_analysis.png
│   ├── sentiment_pie_chart.png
│   ├── confusion_matrix.png
│   ├── training_history.png
│   └── classification_report.txt
├── train.py                      # Training script with MLflow
├── requirements.txt              # Python dependencies
├── mlflow.db                     # MLflow tracking database
└── README.md                     # This file
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model (with MLflow Tracking)

```bash
python train.py
```

This will:
- Load and analyze the IMDB dataset
- Generate data visualizations in `reports/`
- Train a Bidirectional LSTM model
- Log all hyperparameters, metrics, and artifacts to MLflow
- Save the model and tokenizer to `models/`

### 3. View MLflow Experiment Dashboard

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Open: http://127.0.0.1:5000

### 4. Start the API Server

```bash
cd api
python app.py
```

Endpoints available at http://127.0.0.1:8000:
- **API Docs**: http://127.0.0.1:8000/docs
- **Dashboard**: http://127.0.0.1:8000/dashboard
- **Health**: http://127.0.0.1:8000/health

---

## 📊 Core Components

### 1. Deep Learning — LSTM Sentiment Classification

| Parameter         | Value                    |
|-------------------|--------------------------|
| Architecture      | Bidirectional LSTM       |
| Vocab Size        | 10,000                   |
| Embedding Dim     | 128                      |
| LSTM Units        | 64                       |
| Dropout Rate      | 0.3                      |
| Max Sequence Len  | 200                      |
| Optimizer         | Adam                     |
| Loss Function     | Binary Crossentropy      |
| Dataset           | IMDB (50K reviews)       |

**Model Architecture:**
```
Embedding (10000, 128) → Bidirectional LSTM (64) → Dropout (0.3)
→ Bidirectional LSTM (32) → Dropout (0.3) → Dense (64, ReLU)
→ Dropout (0.3) → Dense (1, Sigmoid)
```

### 2. Data Visualization Dashboard

The interactive dashboard (`http://127.0.0.1:8000/dashboard`) includes:

- **📊 KPI Metrics**: Total predictions, positive/negative counts, avg confidence
- **🥧 Sentiment Distribution**: Doughnut chart showing positive vs negative ratio
- **📈 Confidence Trend**: Line chart tracking confidence scores over time
- **📊 Confidence Histogram**: Distribution of model confidence scores
- **💬 Word Cloud**: Most frequent words in analyzed reviews
- **📏 Review Length Analysis**: Word count distribution chart
- **📋 Predictions Table**: Recent prediction history with sentiment badges
- **🔍 Live Prediction**: Real-time review analysis input

### 3. MLOps — Experiment Tracking & Deployment

#### MLflow Integration
- **Experiment Tracking**: All hyperparameters, metrics, and artifacts logged
- **Model Versioning**: Models registered in MLflow Model Registry
- **Metric History**: Per-epoch training/validation accuracy and loss
- **Artifact Storage**: Visualizations, reports, and model files

#### REST API Features
| Endpoint              | Method | Description                    |
|-----------------------|--------|--------------------------------|
| `/`                   | GET    | API status & info              |
| `/health`             | GET    | Model health check             |
| `/predict`            | POST   | Single review prediction       |
| `/batch-predict`      | POST   | Batch prediction               |
| `/predictions`        | GET    | Prediction history             |
| `/analytics/summary`  | GET    | Dashboard analytics data       |
| `/metrics`            | GET    | API monitoring metrics         |
| `/docs`               | GET    | Swagger API documentation      |
| `/dashboard`          | GET    | Interactive visualization      |

#### API Usage Example
```bash
# Single prediction
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"review": "This product is amazing and works perfectly!"}'

# Response:
{
  "timestamp": "2026-03-10T05:30:00",
  "review": "This product is amazing and works perfectly!",
  "sentiment": "Positive",
  "confidence": 0.9234,
  "review_length": 7,
  "latency_ms": 45.2
}
```

---

## 📈 Expected Outcomes

### Model Performance
| Metric     | Score   |
|------------|---------|
| Accuracy   | ~87%    |
| Precision  | ~86%    |
| Recall     | ~88%    |
| F1 Score   | ~87%    |
| AUC-ROC    | ~94%    |

### Generated Reports
- `reports/sentiment_distribution.png` - Class distribution bar chart
- `reports/review_length_analysis.png` - Word count histograms & box plots
- `reports/sentiment_pie_chart.png` - Pie chart of sentiment ratio
- `reports/confusion_matrix.png` - Model confusion matrix
- `reports/training_history.png` - Accuracy & loss curves
- `reports/classification_report.txt` - Detailed classification report

---

## 🛠️ Technology Stack

| Component          | Technology            |
|--------------------|-----------------------|
| Deep Learning      | TensorFlow/Keras      |
| Model Architecture | Bidirectional LSTM    |
| API Framework      | FastAPI               |
| Experiment Tracking| MLflow                |
| Visualization      | Chart.js, Matplotlib, Seaborn |
| Data Processing    | Pandas, NumPy         |
| NLP Preprocessing  | Keras Tokenizer       |
| Dataset            | IMDB Movie Reviews    |

---

## 📝 How to Run Each Component

### Training with Experiment Tracking
```bash
python train.py
```

### MLflow UI
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

### API + Dashboard
```bash
cd api
python app.py
```

### Jupyter Notebook (Alternative Training)
```bash
jupyter notebook notebooks/sentiment_training.ipynb
```

---

## 👨‍💻 Author

**Kashyap Barad** — Lab Practice II (2026)  
Experiment 3: Sentiment Intelligence System for Product Review
