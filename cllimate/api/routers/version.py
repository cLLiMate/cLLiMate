import pkg_resources
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def status():
    return {
        "status": "ok",
        "version": pkg_resources.get_distribution("cllimate").version,
    }
