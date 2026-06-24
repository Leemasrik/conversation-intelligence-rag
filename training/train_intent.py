import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("training/intent_dataset_final.csv")

X = df["text"]
y = df["intent"]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2)
)

X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_vec, y)

# Save
os.makedirs("models", exist_ok=True)

joblib.dump(vectorizer, "models/tfidf.pkl")
joblib.dump(model, "models/intent_model.pkl")

print("Intent classifier trained successfully.")