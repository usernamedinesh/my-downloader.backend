# app/api/v1/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return {"status": "ok", "message": "Video Downloader API is healthy 🚀"}
