from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()


@router.get("/chat")
def chat(From: str = Form(...), Body: str = Form(...)):
    response = MessagingResponse()
    msg = response.message(f"Hi {From}, you said: {Body}")
    return Response(content=str(response), media_type="application/xml")
