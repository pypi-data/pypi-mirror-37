"""Ping wrapper for cross-platform OS ping6 command."""

import os
import sys

from youtube_metrics.lib.net.ping import _linux, _windows


def run(ip_address):
    """Ping an IP 5 times and return values based on the platform.

    Linux returns a dict with keys min, avg, max, mdev

    Keyword arguments:
    ip_address -- the target machine
    """
    result = {}
    if os.name == "posix":
        result = _linux(ip_address, "ping6")
    elif os.name == "nt":
        result = _windows(ip_address)
    else:
        print("[!!!] Unknown os.name", file=sys.stderr)

    return result
