from fastapi import APIRouter

router = APIRouter()


@router.get("/chat")
def chat():
    return "Hello!"
