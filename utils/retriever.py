import pickle
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vectorstore/faiss.index")

with open("vectorstore/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def retrieve(query, top_k=5):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
)

    distances, indices = index.search(
        query_embedding.astype("float32"),
        top_k
    )

    topic_results = []
    chunk_results = []

    for idx in indices[0]:

        item = metadata[idx]

        if item["type"] == "topic":
            topic_results.append(item["data"])

        else:
            chunk_results.append(item["data"])

    return {
        "topics": topic_results,
        "chunks": chunk_results
    }