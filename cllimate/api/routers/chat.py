from fastapi import FastAPI, Form, Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()


@app.post("/hook")
async def chat(From: str = Form(...), Body: str = Form(...)):
   response = MessagingResponse() 
   msg = response.message(f"Hi {From}, you said: {Body}")
   return Response(content=str(response), media_type="application/xml")