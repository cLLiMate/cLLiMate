from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from .articles import search_for_articles

router = APIRouter()


@router.post("/chat")
def chat(From: str = Form(...), Body: str = Form(...)):
    response = MessagingResponse()
    msg = response.message(f"Hi {From}!")
    a = search_for_articles(Body, n_neighbors=5)
    for i in a:
        if (i['url'] != "null"):
            msg = response.message(i['headline'] + "\n" + i['url'])
        else:
            msg = response.message(i['headline'])
    msg = response.message("For more results, visit cLLiMate.tech/search!")
    return Response(content=str(response), media_type="application/xml")