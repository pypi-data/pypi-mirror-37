"""Wrapper for youtube_dl extract_info() function."""

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError


class YTVideoInfo:  # noqa: D101
    def __init__(self):  # noqa: D107
        self._ytdl = YoutubeDL(params={
            "format": "bestvideo",
            "skip_download": True,
            "call_home": False,
            "logtostderr": True,
            "no_color": True
        })

    def get_video_info(self, url):
        """Get video information with youtube_dl.

        Returns a dict with keys "id", "uploader", "title", "duration",
        "view_count", "webpage_url", "url", "ext", "height", "format_note",
        "filesize", "width"

        "error" will contain the same exception youtube_dl raised. In
        this case no other keys are provided.
        """
        try:
            video_info = self._ytdl.process_video_result(
                self._ytdl.extract_info(url, download=False),
                download=False)
        except (DownloadError, ExtractorError) as e:
            return {"error": e}

        video_info["error"] = None
        video_info["duration"] *= 1000  # Normalize to milliseconds
        wanted_keys = ["id", "uploader", "title", "duration", "view_count",
                       "webpage_url", "url", "ext", "height", "format_note",
                       "filesize", "width", "error"]
        retval = {k: v for k, v in video_info.items() if k in wanted_keys}
        return retval
