from os import environ

import pkg_resources
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def status():
    return {
        "status": "ok",
        "version": pkg_resources.get_distribution("cllimate").version,
        "commit_sha": environ.get("COMMIT_SHA", "unknown"),
        "ref_name": environ.get("REF_NAME", "unknown"),
        "namespace": environ.get("NAMESPACE", "development"),
    }
