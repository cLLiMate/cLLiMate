from fastapi import APIRouter, Response
from pydantic import BaseModel

from cllimate.nlp import embed_sentence, get_glove_vector

router = APIRouter()


class EmbedRequest(BaseModel):
    text: str


@router.post("/embed")
def embed(request: EmbedRequest) -> list[float]:
    glove_vector = get_glove_vector()
    return embed_sentence(glove_vector, request.text).tolist()
