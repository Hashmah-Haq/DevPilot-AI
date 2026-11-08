
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent

INDEX_PATH = BASE_DIR / "debugging_index.faiss"
DOCUMENTS_PATH = BASE_DIR / "documents.json"

_model = None
_index = None
_documents = None


def load_rag():
    global _model, _index, _documents

    if not INDEX_PATH.exists() or not DOCUMENTS_PATH.exists():
        raise FileNotFoundError(
            "RAG database missing. Run Step 18 first."
        )

    if _model is None:
        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

    if _index is None:
        _index = faiss.read_index(str(INDEX_PATH))

    if _documents is None:
        with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
            _documents = json.load(f)

    if _index.ntotal != len(_documents):
        raise ValueError("FAISS index and documents do not match.")

    return _model, _index, _documents


def search_knowledge(query, top_k=3):
    model, index, documents = load_rag()

    if not query.strip():
        return []

    top_k = min(max(1, top_k), index.ntotal)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for idx, score in zip(indices[0], scores[0]):
        if idx < 0:
            continue

        results.append({
            "document": documents[int(idx)],
            "similarity": round(float(score), 4)
        })

    return results
