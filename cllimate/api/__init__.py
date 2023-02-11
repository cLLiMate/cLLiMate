from fastapi import FastAPI

from .routers import chat, version

app = FastAPI()
app.include_router(version.router)
app.include_router(chat.router)
