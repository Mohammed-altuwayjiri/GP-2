from pathlib import Path
import joblib

# Project paths
base_dir = Path(__file__).parent
models_dir = base_dir / "models"

# Load trained models and vectorizers
category_model = joblib.load(models_dir / "category_model.pkl")
opinion_model = joblib.load(models_dir / "opinion_model.pkl")
category_vectorizer = joblib.load(models_dir / "category_vectorizer.pkl")
opinion_vectorizer = joblib.load(models_dir / "opinion_vectorizer.pkl")


# Category prediction
def predict_category(text):
    text_vectorized = category_vectorizer.transform([text])
    prediction = category_model.predict(text_vectorized)[0]
    return prediction


# Opinion prediction
def predict_opinion(text):
    text_vectorized = opinion_vectorizer.transform([text])
    prediction = opinion_model.predict(text_vectorized)[0]
    return prediction


# Main review analysis function
def analyze_review(text):
    category = predict_category(text)
    opinion = predict_opinion(text)

    return {
        "category": category,
        "opinion": opinion
    }


# Local test
if __name__ == "__main__":
    sample_text = "The food was delicious and the service was excellent"
    result = analyze_review(sample_text)

    print("Text:", sample_text)
    print("Predicted Category:", result["category"])
    print("Predicted Opinion:", result["opinion"])