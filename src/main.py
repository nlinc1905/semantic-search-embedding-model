import typing as t
import json
import torch
from fastapi import FastAPI, Depends
from fastapi_health import health
from pydantic import BaseModel

from .model import EmbeddingModel


class EmbedRequest(BaseModel):
    text: str


class EmbedBatchRequest(BaseModel):
    texts: t.List[str]


app = FastAPI()
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
model = EmbeddingModel(device=DEVICE)


def get_session():
    return True


def is_start(session: bool = Depends(get_session)):
    """
    Returns True when API has started
    """
    return session


def is_ready(session: bool = Depends(get_session)):
    """
    Returns True when API is ready to receive requests
    """
    return session


def is_alive(session: bool = Depends(get_session)):
    """
    Returns True when API is alive
    """
    return session


# health check endpoints for K8s probes
app.add_api_route('/health_start', health([is_start]))
app.add_api_route('/heath_ready', health([is_ready]))
app.add_api_route('/health_alive', health([is_alive]))


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
