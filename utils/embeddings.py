import json
import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store():

    documents = []
    metadata = []

    # ---------- Topic Summaries ----------

    with open(
        "summaries/topic_summaries.json",
        encoding="utf8"
    ) as f:

        topics = json.load(f)

    for topic in topics:

        documents.append(topic["summary"])

        metadata.append(
            {
                "type": "topic",
                "data": topic
            }
        )

    # ---------- Message Chunks ----------

    with open(
        "summaries/chunks.json",
        encoding="utf8"
    ) as f:

        chunks = json.load(f)

    for chunk in chunks:

        documents.append(chunk["text"])

        metadata.append(
            {
                "type": "chunk",
                "data": chunk
            }
        )

    embeddings = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
)

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
)

    index.add(
        embeddings.astype("float32")
    )

    os.makedirs(
        "vectorstore",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "vectorstore/faiss.index"
    )

    with open(
        "vectorstore/metadata.pkl",
        "wb"
    ) as f:

        pickle.dump(metadata, f)

    print("Vector Store Built")