import typing as t
import json
import torch
from fastapi import FastAPI
from pydantic import BaseModel

from .model import EmbeddingModel


class EmbedRequest(BaseModel):
    text: str


class EmbedBatchRequest(BaseModel):
    texts: t.List[str]


app = FastAPI()
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
model = EmbeddingModel(device=DEVICE)


@app.post("/embed")
def embed(data: EmbedRequest):
    """Synchronous inference on single text sample"""
    embedding = model.embed(text=data.text)
    resp = json.dumps(embedding.tolist())
    return resp


@app.post("/embed_batch")
async def embed_batch(data: EmbedBatchRequest):
    """Async inference on a batch of text samples"""
    embeddings = model.embed_batch(texts=data.texts)
    resp = json.dumps(embeddings.tolist())
    return resp
