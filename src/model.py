import typing as t
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self, device: str):
        self.device = device
        self.model = SentenceTransformer(MODEL_NAME, device=device)

    def embed(self, text: str):
        """
        Single sample inference

        :param text: text to be embedded
        """
        return self.model.encode(text)

    def embed_batch(self, texts: t.List[str]):
        """
        Batch sample inference

        :param texts: texts to be embedded
        """
        return self.model.encode(texts)
