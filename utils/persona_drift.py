import json
import os


POSITIVE_WORDS = [
    "happy", "love", "great", "awesome", "excited",
    "glad", "amazing", "good", "fun", "worth"
]

NEGATIVE_WORDS = [
    "sad", "stress", "frustrated", "angry",
    "sorry", "upset", "hate", "problem",
    "difficult", "hard"
]

CURIOUS_WORDS = [
    "learn", "study", "try", "want",
    "hope", "dream", "moving",
    "new", "planning"
]

PLAYFUL_WORDS = [
    "haha", "lol", "funny", "joke"
]


def detect_mood(text):

    text = text.lower()

    positive = sum(word in text for word in POSITIVE_WORDS)
    negative = sum(word in text for word in NEGATIVE_WORDS)
    curious = sum(word in text for word in CURIOUS_WORDS)
    playful = sum(word in text for word in PLAYFUL_WORDS)

    scores = {
        "Positive": positive,
        "Frustrated": negative,
        "Curious": curious,
        "Playful": playful
    }

    mood = max(scores, key=scores.get)

    if scores[mood] == 0:
        mood = "Neutral"

    return mood


def build_persona_drift():

    with open(
        "persona/personas.json",
        encoding="utf8"
    ) as f:
        personas = json.load(f)

    with open(
        "summaries/topic_summaries.json",
        encoding="utf8"
    ) as f:
        topics = json.load(f)

    grouped_topics = {}

    for topic in topics:

        cid = topic["conversation_id"]

        grouped_topics.setdefault(cid, [])

        grouped_topics[cid].append(topic)

    timeline = []

    previous_mood = None

    for persona in personas:

        cid = persona["conversation_id"]

        day_topics = grouped_topics.get(cid, [])

        full_text = " ".join(
            topic["summary"]
            for topic in day_topics
        )

        mood = detect_mood(full_text)

        message_length = persona["communication_style"]["message_length"]

        if message_length == "Short":
            tone = "Casual"

        elif message_length == "Medium":
            tone = "Balanced"

        else:
            tone = "Formal"

        trigger = "Unknown"

        if day_topics:

            trigger = day_topics[0]["keywords"][0]

        if previous_mood is None:

            drift = "None"

        elif previous_mood == mood:

            drift = "No Change"

        else:

            drift = f"{previous_mood} → {mood}"

        timeline.append({

            "day": cid,

            "conversation_id": cid,

            "previous_mood": previous_mood,

            "current_mood": mood,

            "drift": drift,

            "tone": tone,

            "trigger": trigger

        })

        previous_mood = mood

    os.makedirs("drift", exist_ok=True)

    with open(
        "drift/drift_timeline.json",
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            timeline,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Persona Drift Timeline Created")


if __name__ == "__main__":

    build_persona_drift()