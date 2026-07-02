"""
Sentiment Analysis LSTM Training Script with MLflow Experiment Tracking
=======================================================================
This script trains an LSTM-based sentiment classification model on the 
IMDB dataset and tracks experiments using MLflow.

Usage:
    python train.py
"""

import os
import re
import sys
import pickle
import time
import warnings

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.tensorflow
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report, roc_auc_score
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

warnings.filterwarnings('ignore')

# ============================================================
# Configuration
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "IMDB Dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Hyperparameters
VOCAB_SIZE = 10000
MAX_LEN = 200
EMBEDDING_DIM = 128
LSTM_UNITS = 64
DROPOUT_RATE = 0.3
BATCH_SIZE = 64
EPOCHS = 5
TEST_SIZE = 0.2
RANDOM_STATE = 42

# MLflow Configuration
MLFLOW_TRACKING_URI = f"sqlite:///{os.path.join(BASE_DIR, 'mlflow.db')}"
EXPERIMENT_NAME = "Sentiment-LSTM-Experiment"


def clean_text(text: str) -> str:
    """Clean and preprocess text data."""
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)         # Remove HTML tags
    text = re.sub(r"http\S+", "", text)       # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)   # Keep only letters
    text = " ".join(text.split())              # Remove extra whitespace
    return text


def load_and_prepare_data(data_path: str, sample_size: int = None):
    """Load dataset and perform statistical analysis."""
    print("\n" + "=" * 60)
    print("[STEP 1] Loading and Preparing Data")
    print("=" * 60)

    df = pd.read_csv(data_path)
    print(f"  Dataset shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")

    if sample_size:
        df = df.sample(n=sample_size, random_state=RANDOM_STATE).reset_index(drop=True)
        print(f"  Sampled {sample_size} records for faster training")

    # Statistical Analysis
    print("\n  Sentiment Distribution:")
    sentiment_counts = df['sentiment'].value_counts()
    print(sentiment_counts)

    # Add review length feature
    df['review_length'] = df['review'].apply(lambda x: len(x.split()))
    df['review_char_length'] = df['review'].apply(len)

    print(f"\n  Review Length Statistics:")
    print(f"  Mean word count: {df['review_length'].mean():.1f}")
    print(f"  Median word count: {df['review_length'].median():.1f}")
    print(f"  Min word count: {df['review_length'].min()}")
    print(f"  Max word count: {df['review_length'].max()}")

    # Encode sentiment
    df['label'] = df['sentiment'].map({'positive': 1, 'negative': 0})

    return df, sentiment_counts


def generate_visualizations(df, sentiment_counts, save_dir):
    """Generate and save data visualization plots."""
    print("\n" + "=" * 60)
    print("[STEP 2] Generating Data Visualizations")
    print("=" * 60)

    # 1. Sentiment Distribution Bar Chart
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71', '#e74c3c']
    sentiment_counts.plot(kind='bar', color=colors, ax=ax, edgecolor='black', alpha=0.85)
    ax.set_title('Sentiment Distribution in IMDB Dataset', fontsize=14, fontweight='bold')
    ax.set_xlabel('Sentiment', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_xticklabels(['Positive', 'Negative'], rotation=0)
    for i, v in enumerate(sentiment_counts.values):
        ax.text(i, v + 200, str(v), ha='center', fontweight='bold', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'sentiment_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] Saved: sentiment_distribution.png")

    # 2. Review Length Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].hist(df[df['label'] == 1]['review_length'], bins=50, alpha=0.7,
                 color='#2ecc71', label='Positive', edgecolor='black')
    axes[0].hist(df[df['label'] == 0]['review_length'], bins=50, alpha=0.7,
                 color='#e74c3c', label='Negative', edgecolor='black')
    axes[0].set_title('Review Length Distribution by Sentiment', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Word Count')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()

    df.boxplot(column='review_length', by='sentiment', ax=axes[1],
               patch_artist=True,
               boxprops=dict(facecolor='#3498db', alpha=0.7),
               medianprops=dict(color='red', linewidth=2))
    axes[1].set_title('Review Length Box Plot by Sentiment', fontsize=13, fontweight='bold')
    plt.suptitle('')
    axes[1].set_xlabel('Sentiment')
    axes[1].set_ylabel('Word Count')

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'review_length_analysis.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] Saved: review_length_analysis.png")

    # 3. Pie Chart
    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0.05)
    ax.pie(sentiment_counts.values, labels=['Positive', 'Negative'],
           autopct='%1.1f%%', colors=colors, explode=explode,
           shadow=True, startangle=90, textprops={'fontsize': 13})
    ax.set_title('Sentiment Distribution (Pie Chart)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'sentiment_pie_chart.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] Saved: sentiment_pie_chart.png")

    return [
        os.path.join(save_dir, 'sentiment_distribution.png'),
        os.path.join(save_dir, 'review_length_analysis.png'),
        os.path.join(save_dir, 'sentiment_pie_chart.png'),
    ]


def preprocess_text_data(df):
    """Clean text and prepare sequences for LSTM."""
    print("\n" + "=" * 60)
    print("[STEP 3] Text Preprocessing")
    print("=" * 60)

    print("  Cleaning text data...")
    df['cleaned_review'] = df['review'].apply(clean_text)
    print("  [OK] Text cleaning complete")

    # Tokenization
    print(f"  Tokenizing with vocab_size={VOCAB_SIZE}...")
    tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token='<OOV>')
    tokenizer.fit_on_texts(df['cleaned_review'])
    sequences = tokenizer.texts_to_sequences(df['cleaned_review'])

    # Padding
    print(f"  Padding sequences to max_len={MAX_LEN}...")
    X = pad_sequences(sequences, maxlen=MAX_LEN, padding='post', truncating='post')
    y = df['label'].values

    print(f"  [OK] Input shape: {X.shape}")
    print(f"  [OK] Labels shape: {y.shape}")

    return X, y, tokenizer


def build_lstm_model():
    """Build LSTM model architecture."""
    print("\n" + "=" * 60)
    print("[STEP 4] Building LSTM Model")
    print("=" * 60)

    model = Sequential([
        Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_LEN),
        Bidirectional(LSTM(LSTM_UNITS, return_sequences=True)),
        Dropout(DROPOUT_RATE),
        Bidirectional(LSTM(LSTM_UNITS // 2)),
        Dropout(DROPOUT_RATE),
        Dense(64, activation='relu'),
        Dropout(DROPOUT_RATE),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    model.build(input_shape=(None, MAX_LEN))
    model.summary()
    return model


def train_model(model, X_train, X_test, y_train, y_test):
    """Train the LSTM model with callbacks."""
    print("\n" + "=" * 60)
    print("[STEP 5] Training Model")
    print("=" * 60)

    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=3,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=2,
            verbose=1
        )
    ]

    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )

    return history


def evaluate_model(model, X_test, y_test, save_dir):
    """Evaluate model and generate metrics/plots."""
    print("\n" + "=" * 60)
    print("[STEP 6] Evaluating Model")
    print("=" * 60)

    # Predictions
    y_pred_proba = model.predict(X_test, verbose=0).flatten()
    y_pred = (y_pred_proba > 0.5).astype(int)

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc_roc = roc_auc_score(y_test, y_pred_proba)

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc_roc': auc_roc
    }

    print(f"\n  Model Performance:")
    print(f"  {'─' * 35}")
    for metric_name, metric_val in metrics.items():
        print(f"  {metric_name:>15}: {metric_val:.4f}")
    print(f"  {'─' * 35}")

    # Classification Report
    report = classification_report(y_test, y_pred, target_names=['Negative', 'Positive'])
    print(f"\n  Classification Report:\n{report}")

    # Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Negative', 'Positive'],
                yticklabels=['Negative', 'Positive'])
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] Saved: confusion_matrix.png")

    return metrics, report


def plot_training_history(history, save_dir):
    """Plot training history curves."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2, color='#2ecc71')
    axes[0].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2, color='#e74c3c')
    axes[0].set_title('Model Accuracy Over Epochs', fontsize=13, fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Accuracy')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Loss
    axes[1].plot(history.history['loss'], label='Train Loss', linewidth=2, color='#3498db')
    axes[1].plot(history.history['val_loss'], label='Val Loss', linewidth=2, color='#e67e22')
    axes[1].set_title('Model Loss Over Epochs', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'training_history.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  [OK] Saved: training_history.png")


def save_artifacts(model, tokenizer, models_dir):
    """Save model and tokenizer."""
    print("\n" + "=" * 60)
    print("[STEP 7] Saving Artifacts")
    print("=" * 60)

    model_path = os.path.join(models_dir, "sentiment_lstm_model.h5")
    tokenizer_path = os.path.join(models_dir, "tokenizer.pkl")

    model.save(model_path)
    print(f"  [OK] Model saved: {model_path}")

    with open(tokenizer_path, 'wb') as f:
        pickle.dump(tokenizer, f)
    print(f"  [OK] Tokenizer saved: {tokenizer_path}")

    return model_path, tokenizer_path


def main():
    """Main training pipeline with MLflow tracking."""
    print("\n" + "=" * 60)
    print("SENTIMENT INTELLIGENCE SYSTEM - LSTM TRAINING")
    print("   with MLflow Experiment Tracking")
    print("=" * 60)

    start_time = time.time()

    # Setup MLflow
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    print(f"\n  MLflow Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"  Experiment: {EXPERIMENT_NAME}")

    with mlflow.start_run(run_name=f"LSTM-Train-{time.strftime('%Y%m%d-%H%M%S')}") as run:
        print(f"  Run ID: {run.info.run_id}")

        # Log hyperparameters
        mlflow.log_params({
            'vocab_size': VOCAB_SIZE,
            'max_len': MAX_LEN,
            'embedding_dim': EMBEDDING_DIM,
            'lstm_units': LSTM_UNITS,
            'dropout_rate': DROPOUT_RATE,
            'batch_size': BATCH_SIZE,
            'epochs': EPOCHS,
            'test_size': TEST_SIZE,
            'optimizer': 'adam',
            'loss_function': 'binary_crossentropy',
            'model_type': 'Bidirectional-LSTM'
        })

        # Step 1: Load Data
        df, sentiment_counts = load_and_prepare_data(DATA_PATH)

        # Log dataset info
        mlflow.log_params({
            'dataset_size': len(df),
            'positive_count': int(sentiment_counts.get('positive', 0)),
            'negative_count': int(sentiment_counts.get('negative', 0)),
            'avg_review_length': round(df['review_length'].mean(), 1)
        })

        # Step 2: Visualizations
        viz_paths = generate_visualizations(df, sentiment_counts, REPORTS_DIR)
        for viz_path in viz_paths:
            mlflow.log_artifact(viz_path, "visualizations")

        # Step 3: Preprocess
        X, y, tokenizer = preprocess_text_data(df)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
        )
        print(f"\n  Train set: {X_train.shape[0]} samples")
        print(f"  Test set:  {X_test.shape[0]} samples")

        mlflow.log_params({
            'train_samples': X_train.shape[0],
            'test_samples': X_test.shape[0]
        })

        # Step 4: Build Model
        model = build_lstm_model()
        try:
            mlflow.log_param('total_parameters', model.count_params())
        except Exception:
            mlflow.log_param('total_parameters', 'N/A')

        # Step 5: Train
        history = train_model(model, X_train, X_test, y_train, y_test)

        # Log training metrics per epoch
        for epoch in range(len(history.history['accuracy'])):
            mlflow.log_metrics({
                'train_accuracy': history.history['accuracy'][epoch],
                'train_loss': history.history['loss'][epoch],
                'val_accuracy': history.history['val_accuracy'][epoch],
                'val_loss': history.history['val_loss'][epoch],
            }, step=epoch + 1)

        # Plot training history
        plot_training_history(history, REPORTS_DIR)
        mlflow.log_artifact(os.path.join(REPORTS_DIR, 'training_history.png'), "visualizations")

        # Step 6: Evaluate
        metrics, report = evaluate_model(model, X_test, y_test, REPORTS_DIR)

        # Log final metrics
        mlflow.log_metrics({
            'final_accuracy': metrics['accuracy'],
            'final_precision': metrics['precision'],
            'final_recall': metrics['recall'],
            'final_f1_score': metrics['f1_score'],
            'final_auc_roc': metrics['auc_roc']
        })

        # Log confusion matrix
        mlflow.log_artifact(os.path.join(REPORTS_DIR, 'confusion_matrix.png'), "visualizations")

        # Save classification report
        report_path = os.path.join(REPORTS_DIR, 'classification_report.txt')
        with open(report_path, 'w') as f:
            f.write("=" * 50 + "\n")
            f.write("SENTIMENT ANALYSIS - CLASSIFICATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(report)
            f.write(f"\nAccuracy:  {metrics['accuracy']:.4f}\n")
            f.write(f"Precision: {metrics['precision']:.4f}\n")
            f.write(f"Recall:    {metrics['recall']:.4f}\n")
            f.write(f"F1 Score:  {metrics['f1_score']:.4f}\n")
            f.write(f"AUC-ROC:   {metrics['auc_roc']:.4f}\n")
        mlflow.log_artifact(report_path, "reports")

        # Step 7: Save Model Artifacts
        model_path, tokenizer_path = save_artifacts(model, tokenizer, MODELS_DIR)

        # Log model to MLflow
        mlflow.tensorflow.log_model(model, "sentiment_lstm_model")
        mlflow.log_artifact(tokenizer_path, "model_artifacts")

        # Training Time
        training_time = time.time() - start_time
        mlflow.log_metric('training_time_seconds', training_time)

        print("\n" + "=" * 60)
        print("TRAINING COMPLETE!")
        print("=" * 60)
        print(f"  Run ID:         {run.info.run_id}")
        print(f"  Accuracy:       {metrics['accuracy']:.4f}")
        print(f"  F1 Score:       {metrics['f1_score']:.4f}")
        print(f"  AUC-ROC:        {metrics['auc_roc']:.4f}")
        print(f"  Training Time:  {training_time:.1f}s")
        print(f"\n  View MLflow UI: mlflow ui --backend-store-uri {MLFLOW_TRACKING_URI}")
        print("=" * 60)


if __name__ == "__main__":
    main()
