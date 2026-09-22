import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Project paths
base_dir = Path(__file__).parent
data_path = base_dir / "data" / "training_reviews.csv"
models_dir = base_dir / "models"

models_dir.mkdir(exist_ok=True)

# Read and clean dataset
df = pd.read_csv(data_path, encoding="utf-8-sig")
df = df.dropna(subset=["text", "category", "opinion"])
df["text"] = df["text"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["opinion"] = df["opinion"].astype(str).str.strip()

# Split inputs and labels
X = df["text"]
y_category = df["category"]
y_opinion = df["opinion"]

# Train/test split
X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
    X, y_category, test_size=0.2, random_state=42, stratify=y_category
)

X_train_op, X_test_op, y_train_op, y_test_op = train_test_split(
    X, y_opinion, test_size=0.2, random_state=42, stratify=y_opinion
)

# Text vectorization
category_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
opinion_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

X_train_cat_vec = category_vectorizer.fit_transform(X_train_cat)
X_test_cat_vec = category_vectorizer.transform(X_test_cat)

X_train_op_vec = opinion_vectorizer.fit_transform(X_train_op)
X_test_op_vec = opinion_vectorizer.transform(X_test_op)

# Model training
category_model = LogisticRegression(max_iter=1000)
opinion_model = LogisticRegression(max_iter=1000)

category_model.fit(X_train_cat_vec, y_train_cat)
opinion_model.fit(X_train_op_vec, y_train_op)

# Predictions
y_pred_cat = category_model.predict(X_test_cat_vec)
y_pred_op = opinion_model.predict(X_test_op_vec)

# Evaluation output
category_accuracy = accuracy_score(y_test_cat, y_pred_cat)
opinion_accuracy = accuracy_score(y_test_op, y_pred_op)

print("=== DATASET INFO ===")
print("Rows and Columns:", df.shape)

print("\nCategory Distribution:")
print(df["category"].value_counts())

print("\nOpinion Distribution:")
print(df["opinion"].value_counts())

print("\n=== CATEGORY MODEL RESULTS ===")
print("Category Model Accuracy:", category_accuracy)
print("\nCategory Model Report:")
print(classification_report(y_test_cat, y_pred_cat))

print("\n=== OPINION MODEL RESULTS ===")
print("Opinion Model Accuracy:", opinion_accuracy)
print("\nOpinion Model Report:")
print(classification_report(y_test_op, y_pred_op))

# Save models and vectorizers
joblib.dump(category_model, models_dir / "category_model.pkl")
joblib.dump(opinion_model, models_dir / "opinion_model.pkl")
joblib.dump(category_vectorizer, models_dir / "category_vectorizer.pkl")
joblib.dump(opinion_vectorizer, models_dir / "opinion_vectorizer.pkl")

print("\nModels and vectorizers saved successfully.")