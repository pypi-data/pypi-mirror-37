"""Wrapper for youtube_dl extract_info() function."""

from youtube_dl import YoutubeDL


class YTVideoInfo:  # noqa: D101
    def __init__(self):  # noqa: D107
        self._ytdl = YoutubeDL(params={
            "skip_download": True,
            "call_home": False,
            "quiet": True
        })

    def _filter_formats(self, format_list):
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

        Returns a dict with keys "id", "uploader", "title", "duration",
        "view_count", "webpage_url", "formats" and filters formats to those
        above or equal to 720p. Formats without filesize are also filtered out.

        "formats" list will only contain keys "url", "width", "height",
        "filesize", "ext", "format", and "format_note".
        """
        video_info = self._ytdl.extract_info(url,
                                             download=False,
                                             process=False)
        video_info["formats"] = self._filter_formats(video_info["formats"])
        return {k: v for k, v in video_info.items() if k in ["id",
                                                             "uploader",
                                                             "title",
                                                             "duration",
                                                             "view_count",
                                                             "webpage_url",
                                                             "formats"]}
