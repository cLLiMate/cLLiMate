from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import articles, chat, version

app = FastAPI()
app.include_router(version.router)
app.include_router(chat.router)
app.include_router(articles.router, prefix="/articles", tags=["articles"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
