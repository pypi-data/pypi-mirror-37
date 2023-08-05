import json
import statistics
import sys
from urllib.parse import urlparse

import humanize

from youtube_metrics.lib.convert import dict_to_csv
from youtube_metrics.lib.net import (dns, downloader, local,
                                     quality_measurements)
from youtube_metrics.lib.net.youtube_dl import get_video_info


def _get_unique_caches(format_dicts):
    unique_caches = set()
    for format_dict in format_dicts:
        cache = urlparse(format_dict["url"]).netloc
        unique_caches.add(cache)
    return unique_caches


def main(args):
    if args.output_format not in ["json", "csv"]:
        print("[!!!] Unknown output format: {}".format(args.output_format),
              file=sys.stderr)
        sys.exit(1)

    me = {"ip": local.ip_address()}
    me_geoip_results = quality_measurements.GEOIP2.lookup(me["ip"])
    me.update({"coords": {"lat": me_geoip_results["latitude"],
                          "long": me_geoip_results["longitude"]}})

    dl = downloader.Download()
    downloaded = 0.0
    throughput = 0.0
    results = {"me": me, "videos": []}
    for video in args.video_url:
        print("[+] Processing video: {}".format(video),
              file=sys.stderr)

        yvi = get_video_info.YTVideoInfo()
        video_info = yvi.get_video_info(video)
        if video_info["error"]:
            video_info["error"] = str(video_info["error"])
            print("[!!!] Error occured when trying to fetch video info: {}"
                  .format(video_info["error"]), file=sys.stderr)
        else:
            video_info["error"] = ""
        stats = []

        unique_caches = _get_unique_caches(video_info["formats"])

        print("[+] Video exists in the following cache(s):", file=sys.stderr)
        for cache in unique_caches:
            cache_stats = {"cache_url": cache}
            print("[+]\t{}".format(cache), file=sys.stderr)
            print("[+]\tMeasuring connection quality ...", file=sys.stderr)
            cache_stats.update(quality_measurements.advanced(cache))
            cache_stats["downloads"] = []

            for format_dict in video_info.pop("formats"):
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

                    print("[+]\t{}... -> {}...".format(old_url[:40],
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
                    cache_stats["downloads"].append(download_stats)

                    downloaded = statistics.mean(
                        [x["downloaded"] for x in cache_stats["downloads"]] +
                        [downloaded]
                    )
                    throughput = statistics.mean(
                        [x["throughput"] for x in cache_stats["downloads"]] +
                        [throughput]
                    )

            stats.append(cache_stats)

        results["videos"].append({
                "metadata": video_info,
                "statistics": stats
        })

    print(("[+] Downloaded (avg): {}\n"
           "[+] Throughput (avg): {} per second")
          .format(humanize.naturalsize(downloaded),
                  humanize.naturalsize(throughput)),
          file=sys.stderr)

    if args.output_format == "json":
        results = json.dumps(results)
    else:  # csv
        results = dict_to_csv(results)

    if args.output_file is not None:
        with open(args.output_file, "a+") as fp:
            fp.write(results)
    else:
        print(results)
