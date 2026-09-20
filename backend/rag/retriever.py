# =====================================================
# INDUSTRIAL MAINTENANCE AI
# RAG RETRIEVER
# =====================================================

import chromadb
from pathlib import Path

from backend.rag.embeddings import embedding_function


# =====================================================
# PATH CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PATH = BASE_DIR / "chroma_db"


# =====================================================
# CHROMA CLIENT
# =====================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


# =====================================================
# COLLECTION
# =====================================================

collection = client.get_collection(
    name="industrial_maintenance"
)


# =====================================================
# RETRIEVE DOCUMENTS
# =====================================================

def retrieve_documents(
    query: str,
    top_k: int = 5
):
    """
    Retrieve the most relevant industrial-maintenance
    documents from the Chroma vector database.
    """

    if not query or not query.strip():
        return []

    # -------------------------------------------------
    # CREATE QUERY EMBEDDING
    # -------------------------------------------------

    query_embedding = embedding_function.embed_query(
        query
    )

    # -------------------------------------------------
    # RETRIEVE MORE CANDIDATES
    # -------------------------------------------------
    #
    # Retrieve more candidates internally than the number
    # finally requested. This gives the system a better
    # chance of finding useful technical information.
    #

    candidate_k = max(
        top_k * 2,
        10
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    retrieved = []

    # -------------------------------------------------
    # BUILD RESULT
    # -------------------------------------------------

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        if not document:
            continue

        metadata = metadata or {}

        retrieved.append(
            {
                "text": document,
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "page": metadata.get(
                    "page",
                    "Unknown"
                ),
                "category": metadata.get(
                    "category",
                    "Unknown"
                ),
                "distance": distance
            }
        )

    # -------------------------------------------------
    # SORT BY RELEVANCE
    # -------------------------------------------------
    #
    # Lower distance means greater similarity.
    #

    retrieved.sort(
        key=lambda item: item.get(
            "distance",
            float("inf")
        )
    )

    # -------------------------------------------------
    # RETURN ONLY REQUESTED NUMBER
    # -------------------------------------------------

    return retrieved[:top_k]
