import yt_dlp

def get_video_format(url: str):
    """
    Extract available formats, including complete videos and the single best audio-only option.
    """
    ydl_opts = {
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # 1. Get all formats that have BOTH video and audio
        combined_formats = [
            f for f in info.get("formats", [])
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
        ]

        # 2. Get all audio-only formats
        audio_only_formats = [
            f for f in info.get("formats", [])
            if f.get('vcodec') == 'none' and f.get('acodec') != 'none'
        ]

        final_formats = combined_formats

        # 3. If there are any audio-only formats, find the best one and add it
        if audio_only_formats:
            # Sort by audio bitrate (abr) to find the best quality, descending
            best_audio = sorted(audio_only_formats, key=lambda f: f.get('abr', 0), reverse=True)[0]
            final_formats.append(best_audio)

        # 4. Create the final list of dictionaries for the frontend
        formats_list = [
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                # Label audio-only formats clearly
                "resolution": "Audio Only" if f.get('vcodec') == 'none' else (f.get("resolution") or f"{f.get('width')}x{f.get('height')}"),
                "filesize": f.get("filesize"),
                "direct_url": f.get("url"),
            }
            for f in final_formats
        ]

    return {"title": info.get("title"), "thumbnail": info.get("thumbnail"), "formats": formats_list}


# download video here
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

