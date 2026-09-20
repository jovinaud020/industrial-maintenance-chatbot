from sentence_transformers import SentenceTransformer


# ============================================================
# MULTILINGUAL EMBEDDING MODEL
# ============================================================

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


# ============================================================
# EMBEDDING FUNCTION
# ============================================================

class MultilingualEmbeddingFunction:

    def __init__(self):

        print(
            "Loading multilingual embedding model..."
        )

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        print(
            "Embedding model loaded successfully."
        )

    # ========================================================
    # CHROMADB EMBEDDING FUNCTION NAME
    # ========================================================

    def name(self) -> str:

        return (
            "multilingual-minilm-l12-v2"
        )

    # ========================================================
    # GENERAL EMBEDDING
    # ========================================================

    def __call__(self, input):

        embeddings = self.model.encode(
            input,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    # ========================================================
    # DOCUMENT EMBEDDINGS
    # ========================================================

    def embed_documents(self, input):

        return self.model.encode(
            input,
            normalize_embeddings=True
        ).tolist()

    # ========================================================
    # QUERY EMBEDDING
    # ========================================================

    def embed_query(self, input):

        return self.model.encode(
            [input],
            normalize_embeddings=True
        )[0].tolist()


# ============================================================
# CREATE EMBEDDING FUNCTION
# ============================================================

embedding_function = (
    MultilingualEmbeddingFunction()
)
