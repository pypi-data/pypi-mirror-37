"""Implements converters for data."""
import csv
from io import StringIO

FIELDS = ["my_ip", "my_latitude", "my_longitude",
          "error", "webpage_url", "id", "uploader", "title", "view_count", "duration",  # noqa
          "cache_domain", "cache_ip", "cache_latitude", "cache_longitude",
          "distance",
          "ping_min", "ping_avg", "ping_max", "ping_mdev",
          "download_format", "download_downloaded", "download_throughput",
          "ping_time", "ping6_time", "dns_a_time", "dns_aaaa_time",
          "request_time", "response_time"]


def _flatten_dict(payload):
    new_dicts = []
    for video in payload["videos"]:
        for cache_stats in video["statistics"]:
            for download in cache_stats["downloads"]:
                new_dict = {}
                new_dict["my_ip"] = payload["me"]["ip"]
                new_dict["my_latitude"] = payload["me"]["coords"]["lat"]  # noqa
                new_dict["my_longitude"] = payload["me"]["coords"]["long"]  # noqa
                new_dict["cache_ip"] = download["ip"]
                for ping in cache_stats["pings"]:
                    # Flatten pings
                    if new_dict["cache_ip"] == ping["ip"]:
                        for k, v in ping.items():
                            if k == "ip":
                                continue
                            new_dict["ping_{}".format(k)] = v

                for distance in cache_stats["distances"]:
                    # Flatten distances
                    if distance["ip"] == new_dict["cache_ip"]:
                        new_dict["cache_latitude"] = distance["coordinates"]["lat"]  # noqa
                        new_dict["cache_longitude"] = distance["coordinates"]["long"]  # noqa
                        new_dict["distance"] = distance["distance"]

                # Flatten processing times
                for k, v in cache_stats["processing_time"].items():
                    new_dict[k] = v

                # Flatten video metadata
                for k, v in video["metadata"].items():
                    new_dict[k] = v
                new_dict["cache_domain"] = cache_stats["cache_url"]

                # Flatten downloads
                for k, v in download["processing_time"].items():  # noqa
                    new_dict[k] = v
                for k, v in download.items():
                    if k in ["processing_time", "ip"]:
                        continue
                    new_dict["download_{}".format(k)] = v

                new_dicts.append(new_dict)
    return new_dicts


def dict_to_csv(payload):
    csv_string = StringIO()
    writer = csv.DictWriter(csv_string, fieldnames=FIELDS)
    flattened = _flatten_dict(payload)
    writer.writeheader()
    writer.writerows(flattened)
    return csv_string.getvalue()
