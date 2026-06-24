import joblib

vectorizer = joblib.load(
    "models/tfidf.pkl"
)

model = joblib.load(
    "models/intent_model.pkl"
)


def predict_intent(text):

    vector = vectorizer.transform(
        [text]
    )

    prediction = model.predict(
        vector
    )[0]

    return prediction