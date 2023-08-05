import argparse
import statistics
import json
import sys
from urllib.parse import urlparse

import humanize

from youtube_metrics.lib.net import (dns, downloader, local,
                                     quality_measurements)
from youtube_metrics.lib.net.youtube_dl import get_video_info


def _get_unique_caches(format_dicts):
    unique_caches = set()
    for format_dict in format_dicts:
        cache = urlparse(format_dict["url"]).netloc
        unique_caches.add(cache)
    return unique_caches


def main():
    parser = argparse.ArgumentParser(
        description="Gather metrics about a video download.")
    parser.add_argument("video_url", type=str, nargs="+",
                        help=("The target video to download. Supports same "
                              "services as youtube_dl."))
    parser.add_argument(
        "--chunk-size", "-c",
        help=("Bytesize of each downloaded chunks (each chunk is timed). "
              "Default: 1024"),
        default=1024)
    parser.add_argument(
        "--download-limit", "-l",
        help=("Bytesize of the maximum download before stopping measurements. "
              "Default: 41943040"),
        default=41943040)
    args = parser.parse_args()

    me = {"ip": local.ip_address()}
    me_geoip_results = quality_measurements.GEOIP2.lookup(me["ip"])
    me.update({"coords": {"lat": me_geoip_results["latitude"],
                          "long": me_geoip_results["longitude"]}})

    dl = downloader.Download()

    results = {"me": me, "videos": {}}
    for video in args.video_url:
        print("[+] Processing video: {}".format(video),
              file=sys.stderr)
        yvi = get_video_info.YTVideoInfo()
        video_info = yvi.get_video_info(video)
        analysis = {}

        domains = _get_unique_caches(video_info["formats"])

        print("[+] Video exists in the following cache(s):", file=sys.stderr)
        for domain in domains:
            print("[+]\t{}".format(domain), file=sys.stderr)
            print("[+]\tMeasuring connection quality ...", file=sys.stderr)
            analysis[domain] = quality_measurements.advanced(domain)
            analysis[domain]["downloads"] = []

        for format_dict in video_info["formats"]:
            print("[+] Resolving format download URL ...",
                  file=sys.stderr)

            domain = urlparse(format_dict["url"]).netloc
            domain_a_records = dns.a_query(domain)
            domain_aaaa_records = dns.aaaa_query(domain)
            _format = "{}_{}".format(format_dict["ext"],
                                     format_dict["format_note"])
            for ip_address in set(domain_a_records + domain_aaaa_records):
                old_url = format_dict["url"]
                new_url = old_url.replace(domain, ip_address)
                new_domain = urlparse(new_url).netloc

                print("[+]\t {}... -> {}...".format(old_url[:40],
                                                    new_url[:40]),
                      file=sys.stderr)
                print(("[+]\tMeasuring connection bandwidth to {} "
                       "for video format {}").format(new_domain, _format),
                      file=sys.stderr)

                download_stats = dl.run(format_dict["url"],
                                        int(args.chunk_size),
                                        int(args.download_limit))
                download_stats["ip"] = new_domain
                download_stats["format"] = _format
                analysis[domain]["downloads"].append(download_stats)

        downloaded = humanize.naturalsize(statistics.mean(
            [x["downloaded"] for x in analysis[domain]["downloads"]]
        ))
        throughput = humanize.naturalsize(statistics.mean(
            [x["throughput"] for x in analysis[domain]["downloads"]]
        ))
        print(("[+] Downloaded (avg): {}\n"
               "[+] Throughput (avg): {} per second").format(downloaded,
                                                             throughput),
              file=sys.stderr)

        results["videos"].update({video: {"caches": analysis}})

    print(json.dumps(results))
