from sentence_transformers import SentenceTransformer


MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


class MultilingualEmbeddingFunction:

    def __init__(self):

        self.model = None

    def _load_model(self):

        if self.model is None:

            print("Loading multilingual embedding model...")

            self.model = SentenceTransformer(
                MODEL_NAME,
                device="cpu"
            )

            print(
                "Embedding model loaded successfully."
            )

    def name(self) -> str:

        return "multilingual-minilm-l12-v2"

    def __call__(self, input):

        self._load_model()

        embeddings = self.model.encode(
            input,
            normalize_embeddings=True
        )

        return embeddings.tolist()

    def embed_documents(self, input):

        self._load_model()

        return self.model.encode(
            input,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, input):

        self._load_model()

        return self.model.encode(
            [input],
            normalize_embeddings=True
        )[0].tolist()


embedding_function = MultilingualEmbeddingFunction()