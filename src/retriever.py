import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class FAISSRetriever:

    def __init__(self):

        print("Loading model...")
        self.model = SentenceTransformer(
            "intfloat/multilingual-e5-small"
        )

        print("Loading index...")
        self.index = faiss.read_index("data/faiss.index")

        print("Loading chunks...")
        self.chunks = json.load(
            open("data/chunks.json", encoding="utf-8")
        )

    def search(self, query, k=3):

        # E5 query format
        q = "query: " + query

        q_vec = self.model.encode(
            [q],
            normalize_embeddings=True
        )

        scores, ids = self.index.search(
            np.array(q_vec, dtype=np.float32),
            k
        )

        results = []

        for i, score in zip(ids[0], scores[0]):

            chunk = self.chunks[i]

            results.append({
                "score": float(score),
                "text": chunk["text"],
                "metadata": chunk.get("metadata", {})
            })

        return results