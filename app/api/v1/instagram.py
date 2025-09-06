from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, JSONResponse
import requests
from app.services.instagram_service import download_instagram_video, get_video_format
from unidecode import unidecode

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
async def download(url: str, format_id: str):
    """
    Streams the requested video format directly to the client for download.
    The video file is not saved on the server.
    """
    try:
        data = download_instagram_video(url, format_id)

        if "direct_url" in data and data["direct_url"]:

            # -- FIX STARTS HERE --

            # 1. Get the original title
            original_title = data.get("title", "video")

            # 2. Sanitize the title to remove special characters
            # unidecode will convert special characters (like é, ñ, 😊) to their closest ASCII equivalent
            safe_title = unidecode(original_title)

            # -- FIX ENDS HERE --

            resp = requests.get(data["direct_url"], stream=True)

            return StreamingResponse(
                resp.iter_content(chunk_size=1024 * 1024),
                media_type="video/mp4",
                # Use the new 'safe_title' for the filename
                headers={"Content-Disposition": f'attachment; filename="{safe_title}.mp4"'}
            )

        return JSONResponse(content={"error": "Format not found or direct URL is missing"}, status_code=404)

    except Exception as e:
        # It's good practice to wrap this endpoint in a try/except block as well
        return JSONResponse(content={"error": str(e)}, status_code=500)

