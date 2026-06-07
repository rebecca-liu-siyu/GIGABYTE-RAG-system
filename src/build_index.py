import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def load_chunks(path="data/chunks.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_embeddings(model, chunks):
    texts = [
        "passage: " + c["text"]
        for c in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return np.array(embeddings, dtype=np.float32)


def main():

    print("Loading chunks...")
    chunks = load_chunks()

    print("Loading embedding model...")
    model = SentenceTransformer("intfloat/multilingual-e5-small")

    print("Encoding...")
    vectors = build_embeddings(model, chunks)

    dim = vectors.shape[1]

    print("Building FAISS index...")

    index = faiss.IndexFlatIP(dim)  # cosine similarity (因為 normalize)
    index.add(vectors)

    faiss.write_index(index, "data/faiss.index")

    # save chunks for retrieval mapping
    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print("DONE: FAISS index built")


if __name__ == "__main__":
    main()