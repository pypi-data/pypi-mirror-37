# flake8: noqa

def main():
    import argparse

    from youtube_metrics.es import main as es
    from youtube_metrics.analyze import main as analyze

    parser = argparse.ArgumentParser(
        description="Gather metrics about a video download.")
    subparsers = parser.add_subparsers()
    parser_v = subparsers.add_parser("analyze", help="Analyze video")
    parser_v.set_defaults(func=analyze)
    parser_e = subparsers.add_parser("es", help="Print ES template")
    parser_e.set_defaults(func=es)
    parser_v.add_argument("video_url", type=str, nargs="+",
                          help=("The target video to download. Supports same "
                                "services as youtube_dl."))
    parser_v.add_argument(
        "--chunk-size", "-c",
        help=("Bytesize of each downloaded chunks (each chunk is timed). "
              "Default: 1024"),
        default=1024)
    parser_v.add_argument(
        "--download-limit", "-l",
        help=("Bytesize of the maximum download before stopping measurements. "
              "Default: 41943040"),
        default=41943040)
    parser_v.add_argument(
        "--output-file", "-of",
        help=("Filepath for output. Output will be appended to the file. "
              "If not defined, stdout is used"),
        default=None
    )
    parser_v.add_argument(
        "--output-format", "-o",
        help=("Format for output. Valid values: json, csv, bulk-es. Default: json"),
        default="json"
    )
    args = parser.parse_args()
    args.func(args)
