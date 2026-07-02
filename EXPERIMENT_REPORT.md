# Experiment 3: Sentiment Intelligence System for Movie Reviews

**Lab Practice II (2026) | Author: Kashyap Barad | Date: March 10, 2026**

---

## 1. Objective

To build an end-to-end sentiment analysis system that classifies IMDB movie reviews as **Positive** or **Negative** using a Bidirectional LSTM deep learning model, visualize results through interactive dashboards (Power BI + Web), and manage experiments using MLOps practices with MLflow.

## 2. Dataset

The **IMDB Movie Review Dataset** (50,000 reviews — 25K Positive, 25K Negative) was used. Reviews were preprocessed by lowercasing, removing HTML tags and special characters, tokenizing into sequences of the top 10,000 words, and padding/truncating to a fixed length of 200 tokens. The data was split 80/20 (40K train, 10K test) with stratified sampling.

## 3. Model Architecture & Training

A **Bidirectional LSTM** was chosen because it reads text both forward and backward, capturing richer context than standard LSTMs. The architecture consists of an Embedding layer (10,000 × 128), two stacked Bidirectional LSTM layers (64 and 32 units), Dropout layers (0.3) for regularization, and a final Sigmoid output layer for binary classification. The model has ~1.4M trainable parameters.

Training used the **Adam optimizer** with binary crossentropy loss over 5 epochs. **Early Stopping** (patience=3) monitored validation loss and restored the best weights from Epoch 2, where overfitting was detected — training accuracy reached 96.6% while validation plateaued at ~86%.

## 4. Results

| Metric | Score |
|--------|-------|
| **Accuracy** | **85.99%** |
| **Precision** | **89.91%** |
| **Recall** | **81.08%** |
| **F1 Score** | **85.27%** |
| **AUC-ROC** | **93.93%** |

The model correctly classifies ~86% of reviews. It has higher precision for positive reviews (0.90) and higher recall for negative reviews (0.91), meaning it is conservative when labeling reviews as positive. The 93.93% AUC-ROC indicates excellent discriminatory power.

## 5. Optimization Techniques

- **Early Stopping** — Prevented overfitting by restoring best weights when validation loss stopped improving
- **ReduceLROnPlateau** — Halved learning rate when training stalled, enabling finer convergence
- **Dropout (0.3)** — Applied after each LSTM and Dense layer to reduce over-reliance on specific neurons
- **Bidirectional Processing** — Doubled contextual information compared to unidirectional LSTM
- **Stratified Splitting** — Maintained equal class distribution in train/test sets

## 6. MLOps — Experiment Tracking (MLflow)

All experiments are tracked using **MLflow** (accessible at `http://127.0.0.1:5000`). Each training run logs: hyperparameters (vocab_size, LSTM units, dropout, batch size, epochs), per-epoch metrics (accuracy, loss for train and validation), final evaluation metrics (accuracy, precision, recall, F1, AUC-ROC), and artifacts (trained model, tokenizer, all visualization plots, classification report). This ensures every experiment is **reproducible** — any past run can be compared, replicated, or rolled back.

## 7. Data Visualization & Power BI Integration

### Web Dashboard (Real-time)
An interactive dashboard at `http://127.0.0.1:8000/dashboard` provides real-time visualization using **Chart.js**. It includes 5 KPI cards, a gauge chart (sentiment health), donut chart (sentiment split), trend line chart, scatter plot (confidence vs length), grouped bar chart, word cloud, and a predictions table — all cross-filtered by **3 interactive slicers** (Sentiment, Confidence Level, Review Length).

### Power BI Dashboard (Enterprise Analytics)
The model's predictions are exported to `predictions_log.csv`, which is imported into **Power BI Desktop** using **Get Data → Text/CSV**. The following Power BI features are used:

| Feature | Purpose |
|---------|---------|
| **Power Query Editor** | Transform timestamps, create derived columns (Date, confidence_category, length_bucket) |
| **DAX Measures** | Calculate KPIs — Total Reviews, Positive %, Sentiment Ratio using formulas like `CALCULATE`, `DIVIDE`, `AVERAGE` |
| **Slicers (×4)** | Interactive filters — Sentiment dropdown, Date range slider, Confidence dropdown, Review length buttons |
| **Card, Gauge, Donut, Line, Bar, Scatter, Table Visuals** | 14 visualization types displaying sentiment metrics, trends, distributions |
| **Word Cloud (AppSource)** | Custom visual showing most frequent review keywords |
| **Conditional Formatting** | Green/Red backgrounds for sentiment, data bars for confidence scores |
| **Sync Slicers & Edit Interactions** | Consistent filters across 3 report pages; control which visuals each slicer affects |

### Integration Pipeline
The LSTM model feeds Power BI through a simple pipeline: **User submits review → FastAPI `/predict` endpoint → LSTM model classifies sentiment → Result appended to `predictions_log.csv` → Power BI imports CSV and visualizes with DAX measures, slicers, and charts**. The web dashboard uses the same data via the API's `/analytics/summary` endpoint with auto-refresh every 30 seconds.

## 8. Deployment (REST API)

The model is deployed via **FastAPI** at `http://127.0.0.1:8000` with endpoints for single prediction (`/predict`), batch prediction (`/batch-predict`), historical data (`/predictions`), analytics (`/analytics/summary`), monitoring (`/metrics`, `/health`), and the dashboard (`/dashboard`). API documentation is auto-generated at `/docs`.

## 9. Conclusion

The Sentiment Intelligence System successfully classifies movie reviews with **85.99% accuracy** and **93.93% AUC-ROC** using a Bidirectional LSTM. Interactive dashboards (Web + Power BI) with dynamic slicers enable non-technical stakeholders to explore sentiment trends, confidence patterns, and keyword analysis. MLflow ensures full experiment reproducibility. Future enhancements include Transformer models (BERT) for higher accuracy and aspect-based sentiment analysis for granular insights into acting, story, and cinematography.

---

**Technology Stack:** Python, TensorFlow/Keras, FastAPI, MLflow, Chart.js, Power BI, Pandas, Scikit-learn, Matplotlib, Seaborn
