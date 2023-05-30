import unittest
import torch

from src.model import EmbeddingModel


class EmbeddingModelTestCase(unittest.TestCase):

    def setUp(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = EmbeddingModel(device=self.device)

    def test_embed(self):
        text = "string"
        result = self.model.embed(text=text)
        assert result.shape == (384,)

    def test_embed_batch(self):
        texts = ["apples", "bananas"]
        result = self.model.embed_batch(texts=texts)
        assert result.shape == (2, 384)
