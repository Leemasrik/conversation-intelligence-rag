POSITIVE = [
    "happy",
    "love",
    "great",
    "awesome",
    "good",
    "excited",
    "amazing",
    "glad",
    "enjoy"
]

NEGATIVE = [
    "sad",
    "cry",
    "stress",
    "angry",
    "hate",
    "worried",
    "upset",
    "frustrated",
    "depressed"
]


def emotion_score(text):

    text = text.lower()

    score = 1

    for word in POSITIVE:

        if word in text:
            score += 2

    for word in NEGATIVE:

        if word in text:
            score += 3

    return score