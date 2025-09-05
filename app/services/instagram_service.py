import yt_dlp

def get_video_format(url: str):
    """
    Extract available formats from an Instagram video.
    """
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "resolution": f.get("resolution") or f"{f.get('width')}x{f.get('height')}",
                "filesize": f.get("filesize"),
                "direct_url": f.get("url"),
            }
            for f in info.get("formats", [])
        ]
    return {"title": info.get("title"),"thumbnail":info.get("thumbnail") , "formats": formats}


def download_instagram_video(url: str, format_id: str = "best"):
    """
    Return direct download URL for the requested format.
    """
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        for f in info.get("formats", []):
            if f.get("format_id") == format_id:
                return {"title": info.get("title"), "direct_url": f.get("url")}
    return {"error": "Format not found"}

