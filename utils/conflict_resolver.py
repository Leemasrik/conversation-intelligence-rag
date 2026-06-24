from utils.retriever import retrieve

import re


POSITIVE = [
    "happy","love","great","good",
    "awesome","excited","glad",
    "amazing","enjoy"
]

NEGATIVE = [
    "sad","angry","stress",
    "upset","cry","hate",
    "worried","frustrated"
]

NEGATIONS = [
    "not",
    "never",
    "no",
    "don't",
    "didn't",
    "can't",
    "isn't"
]
STOPWORDS = {
    "did","do","does","have","has","had",
    "anything","about","mention",
    "mentioned","tell","me","my",
    "the","a","an","is","are",
    "was","were"
}


def extract_entity(query):

    words = re.findall(r"\w+", query.lower())

    entities = [
        word
        for word in words
        if word not in STOPWORDS
    ]

    if entities:
        return entities[-1]

    return None
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
def detect_conflicts(topics):

    conflicts = []

    for i in range(len(topics)-1):

        first = topics[i]["summary"].lower()

        second = topics[i+1]["summary"].lower()

        first_neg = any(
            word in first
            for word in NEGATIONS
        )

        second_neg = any(
            word in second
            for word in NEGATIONS
        )

        if first_neg != second_neg:

            conflicts.append({

                "earlier":topics[i],

                "later":topics[i+1]

            })

    return conflicts
def resolve(query):

    results = retrieve(query, top_k=10)

    topics = results["topics"]

    chunks = results["chunks"]

    if not topics:

        return None

    entity = extract_entity(query)

    timeline = sorted(

        topics,

        key=lambda x:x["conversation_id"]

    )

    ranked_chunks = sorted(

        chunks,

        key=lambda x:emotion_score(
            x["text"]
        ),

        reverse=True

    )

    conflicts = detect_conflicts(
        timeline
    )

    return {

        "entity":entity,

        "timeline":timeline,

        "evidence":ranked_chunks[:5],

        "conflicts":conflicts

    }