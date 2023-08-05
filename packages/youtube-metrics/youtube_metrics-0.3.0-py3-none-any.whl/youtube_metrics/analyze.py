import json
import statistics
import sys
import datetime
from urllib.parse import urlparse

import humanize

from youtube_metrics.lib.convert import dict_to_csv
from youtube_metrics.lib.net import downloader, local, quality_measurements
from youtube_metrics.lib.net.youtube_dl import get_video_info


def _get_unique_caches(format_dicts):
    unique_caches = set()
    for format_dict in format_dicts:
        cache = urlparse(format_dict["url"]).netloc
        unique_caches.add(cache)
    return unique_caches


def main(args):
    if args.output_format not in ["json", "csv", "bulk-es"]:
        print("[!!!] Unknown output format: {}".format(args.output_format),
              file=sys.stderr)
        sys.exit(1)

    me = {"ip": local.ip_address()}
    me_geoip_results = quality_measurements.GEOIP2.lookup(me["ip"])
    me.update({"coords": {"lat": me_geoip_results["latitude"],
                          "lon": me_geoip_results["longitude"]}})
    me.update({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()})

    dl = downloader.Download()
    downloaded = []
    throughput = []
    results = []
    for video in args.video_url:
        result = {"me": me, "video": {}}
        print("[+] Processing video: {}".format(video),
              file=sys.stderr)

        yvi = get_video_info.YTVideoInfo()
        video_info = yvi.get_video_info(video)
        if video_info["error"]:
            video_info["error"] = str(video_info["error"])
            print("[!!!] Error occured when trying to fetch video info: {}"
                  .format(video_info["error"]), file=sys.stderr)
            continue
        else:
            video_info["error"] = ""

        cache = video_info["url"]
        domain = urlparse(cache).netloc
        cache_stats = {"cache_url": domain}
        print("[+] Resolved best quality cache to: {}".format(cache),
              file=sys.stderr)
        print("[+] Measuring connection quality ...", file=sys.stderr)
        cache_stats.update(quality_measurements.advanced(domain))
        cache_stats["download"] = {}
        print("[+] Measuring bandwidth ...", file=sys.stderr)
        domain = urlparse(cache).netloc
        _format = "{}_{}".format(video_info["ext"],
                                 video_info["format_note"])
        download_stats = dl.run(cache,
                                int(args.chunk_size),
                                int(args.download_limit))
        download_stats["format"] = _format
        cache_stats["download"] = download_stats

        downloaded.append(cache_stats["download"]["downloaded"])
        throughput.append(cache_stats["download"]["throughput"])

        result["video"] = {
               "metadata": video_info,
               "statistics": cache_stats
        }
        result["video"]["metadata"]["webpage"] = (
            result["video"]["metadata"].pop("webpage_url"))
        result["video"]["statistics"]["cache"] = (
            result["video"]["statistics"].pop("cache_url"))
        results.append(result)
    if args.output_format == "json":
        for result in results:
            result = json.dumps(result)
            if args.output_file is not None:
                with open(args.output_file, "a+") as fp:
                    fp.write(result + "\n")
            else:
                print(result)
    elif args.output_format == "bulk-es":

        for result in results:
            header_json = json.dumps({
                "index": {
                    "_index": "ytmetrics-{}".format(
                        result["me"]["timestamp"].split("T")[0]
                    ),
                    "_type": "_doc"
                }
            })
            result_json = json.dumps(result)
            if args.output_file is not None:
                with open(args.output_file, "a+") as fp:
                    fp.write(header_json + "\n")
                    fp.write(result_json + "\n")
            else:
                print(header_json)
                print(result_json)
    else:
        result = dict_to_csv(results)
        if args.output_file is not None:
            with open(args.output_file, "a+") as fp:
                fp.write(result)
        else:
            print(result)

    print(("[+] Downloaded (avg): {}\n"
           "[+] Throughput (avg): {} per second")
          .format(humanize.naturalsize(statistics.mean(downloaded)),
                  humanize.naturalsize(statistics.mean(throughput))),
          file=sys.stderr)
