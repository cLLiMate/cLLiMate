import functools
import os
import pickle
from typing import Union

import numpy as np
import pandas as pd
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.neighbors import NearestNeighbors

from cllimate.nlp import embed_sentence, get_glove_vector

router = APIRouter()


class EmbedRequest(BaseModel):
    text: str


@functools.lru_cache(maxsize=16)
def _embed(text: str) -> np.ndarray:
    gv = get_glove_vector()
    return embed_sentence(gv, text)


def _get_base_url() -> str:
    try:
        base_url = os.environ["VITE_STATIC_HOST"]
    except KeyError:
        raise ValueError("VITE_STATIC_HOST is not set")
    return base_url


@functools.cache
def _get_article_df() -> pd.DataFrame:
    base_url = _get_base_url()
    df = pd.read_parquet(f"{base_url}/data/processed/news-consolidated-v2.parquet")
    return df


@functools.cache
def _get_knn_model(model_name) -> NearestNeighbors:
    # load model from disk by unpickling from a remote URL
    base_url = _get_base_url()
    url = f"{base_url}/data/models/knn/v2/{model_name}.pkl"
    r = requests.get(url, allow_redirects=True, stream=True)
    try:
        model = pickle.loads(r.content)
    except:
        raise ValueError(f"Model {model_name} not found, {url}")
    return model


class ArticleResponse(BaseModel):
    id: int
    source: str
    date: str
    headline: str
    embedding: Union[list[float], None]
    url: str
    sentiment_score: float
    sentiment_label: str


class ArticleSearchResponse(BaseModel):
    """The same as a single article, but without the embedding and with the index + distance"""

    id: int
    source: str
    date: str
    headline: str
    url: str
    sentiment_score: float
    sentiment_label: str
    distance: float


@router.post("/embed")
def embed(request: EmbedRequest) -> list[float]:
    return _embed(request.text).tolist()


@router.get("/entry/{article_id}")
def get_article(article_id: int) -> ArticleResponse:
    df = _get_article_df()
    entry = df[df["id"] == article_id].to_dict(orient="records")[0]
    entry["date"] = entry["date"].strftime("%Y-%m-%d")
    entry["embedding"] = entry["embedding"].tolist()
    return entry


@router.post("/search")
def search(
    request: EmbedRequest, n_neighbors: int = 20, label: str = "all"
) -> list[ArticleResponse]:
    model = _get_knn_model(label)
    embedding = _embed(request.text)
    distances, indices = model.kneighbors([embedding], n_neighbors=n_neighbors)

    df = _get_article_df()
    subset = df.iloc[indices[0]].drop(columns=["embedding"])
    subset["distance"] = distances[0]
    subset["date"] = subset["date"].dt.strftime("%Y-%m-%d")
    return subset.to_dict(orient="records")
