from fastapi import FastAPI

from .routers import articles, chat, version

app = FastAPI()
app.include_router(version.router)
app.include_router(chat.router)
app.include_router(articles.router, prefix="/articles", tags=["articles"])
