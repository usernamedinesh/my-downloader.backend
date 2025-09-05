from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.services.instagram_service import download_instagram_video, get_video_format

router = APIRouter()

@router.get("/formats")
async def formats(url: str = Query(..., description="Instagram video URL")):
    """
    Get available formats for an Instagram video.
    """
    try:
        data = get_video_format(url)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/download")
async def download(url: str, format_id: str = "best"):
    """
    Download Instagram video (returns direct download link).
    """
    try:
        data = download_instagram_video(url, format_id)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

