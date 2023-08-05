"""Wrapper for youtube_dl extract_info() function."""

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError


class YTVideoInfo:  # noqa: D101
    def __init__(self):  # noqa: D107
        self._ytdl = YoutubeDL(params={
            "skip_download": True,
            "call_home": False,
            "logtostderr": True,
            "no_color": True
        })

    def _filter_formats(self, format_list, orig_url):
        formats = filter(lambda k: k.get("height", 0) >= 720 and
                         "filesize" in k, format_list)
        return [{"url": d.get("url"),
                 "width": d.get("width"),
                 "height": d.get("height"),
                 "filesize": d.get("filesize"),
                 "format_id": d.get("format_id"),
                 "ext": d.get("ext"),
                 "format_note": d.get("format_note")} for d in formats]

    def get_video_info(self, url):
        """Get video information with youtube_dl.

        Returns a dict with keys "error", "id", "uploader", "title",
        "duration", "view_count", "webpage_url", "formats" and filters
        formats to those above or equal to 720p. Formats without filesize are
        also filtered out.

        "formats" list will only contain keys "url", "width", "height",
        "filesize", "ext", "format", and "format_note".

        "error" will contain the same exception youtube_dl raised. In
        this case, all the other keys exists but the values are None,
        except "webpage_url" which will contain the original url that
        the user requested. "formats" list will be empty.
        """
        try:
            video_info = self._ytdl.extract_info(url,
                                                 download=False,
                                                 process=False)
        except (DownloadError, ExtractorError) as e:
            return {"id": None, "uploader": None, "title": None,
                    "duration": None, "view_count": None, "webpage_url": url,
                    "formats": [], "error": e}
        video_info["formats"] = self._filter_formats(video_info["formats"],
                                                     url)
        if not video_info["formats"]:
            video_info["error"] = ExtractorError(
                msg="Video does not have formats >= 720p",
                expected=True
            )
        else:
            video_info["error"] = None

        video_info["duration"] *= 1000  # Normalize to milliseconds
        return {k: v for k, v in video_info.items() if k in ["id",
                                                             "uploader",
                                                             "title",
                                                             "duration",
                                                             "view_count",
                                                             "webpage_url",
                                                             "formats",
                                                             "error"]}
