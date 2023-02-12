import functools
import os
from typing import Union

import numpy as np
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

from cllimate.nlp import embed_sentence, get_glove_vector

router = APIRouter()


class EmbedRequest(BaseModel):
    text: str


def _embed(text: str) -> np.ndarray:
    gv = get_glove_vector()
    return embed_sentence(gv, text)


def _get_article_df() -> pd.DataFrame:
    try:
        base_url = os.environ["VITE_STATIC_HOST"]
    except KeyError:
        raise ValueError("VITE_STATIC_HOST is not set")

    df = pd.read_parquet(f"{base_url}/data/processed/news-consolidated-v2.parquet")
    return df


class ArticleResponse(BaseModel):
    id: int
    source: str
    date: str
    headline: str
    embedding: Union[list[float], None]
    url: str
    sentiment_score: float
    sentiment_label: str


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
