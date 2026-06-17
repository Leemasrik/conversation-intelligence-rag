from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def detect_topics(messages, window_size=5, threshold=0.40):
    """
    Split a conversation into semantic topics.
    """

    windows = []

    for i in range(0, len(messages), window_size):

        text = " ".join(
            [
                m["text"]
                for m in messages[i:i+window_size]
            ]
        )

        windows.append(text)

    embeddings = model.encode(
        windows,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    topics = []

    start_window = 0

    for i in range(1, len(embeddings)):

        sim = cosine_similarity(
            [embeddings[i-1]],
            [embeddings[i]]
        )[0][0]

        if sim < threshold:

            topics.append({
                "start": start_window * window_size,
                "end": min(i * window_size - 1, len(messages)-1)
            })

            start_window = i

    topics.append({
        "start": start_window * window_size,
        "end": len(messages)-1
    })

    return topics