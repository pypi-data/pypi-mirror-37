"""Downloads a file."""

import time

import urllib3


class Download:
    """Download a file using urllib3. Calculates transfer rate."""

    def __init__(self, proxy=None):
        """Initialize a downloader.

        Keyword arguments:
        proxy -- proxy_url for urllib3 ProxyManager
        """
        headers = {"User-Agent": "youtube-metrics"}
        if proxy:
            self._http = urllib3.ProxyManager(proxy_url=proxy, headers=headers)
        else:
            self._http = urllib3.PoolManager(headers=headers)

    def run(self, url, chunk_size=1024, download_limit=41943040):
        """Download a file.

        Keyword arguments:
        chunk_size -- size of each downloaded chunks (each chunk is timed).
                      Default 1 kiB
        download_limit -- size of the maximum download before aborting.
                          Default 40 MiB
        """
        start_request = time.time()
        req = self._http.request("GET", url, preload_content=False)
        end_request = time.time()

        response = []

        allowed_downloads = round(download_limit / chunk_size)
        chunks = 0

        start_response = time.time()
        for chunk in req.stream(chunk_size):
            if chunks == allowed_downloads:
                break
            response.append(chunk)
            chunks += 1
        end_response = time.time()

        req.release_conn()

        upload_time = end_request - start_request
        download_time = end_response - start_response
        downloaded_bytes = sum([len(_) for _ in response])

        return {"downloaded": downloaded_bytes,
                "throughput": downloaded_bytes / download_time,
                "processing_time": {"request_time": upload_time * 1000,
                                    "response_time": download_time * 1000}}
