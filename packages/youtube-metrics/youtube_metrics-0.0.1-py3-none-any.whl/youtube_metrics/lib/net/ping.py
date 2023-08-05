"""Ping wrapper for cross-platform OS ping command."""

import os
import re
import subprocess
import sys


def _run_ping(match_pattern, executable):
    try:
        result = subprocess.check_output(executable)
    except subprocess.CalledProcessError as e:
        print("[!!!] ping exited with code {}".format(e.returncode),
              file=sys.stderr)
        print("[!!!] ping returned:", file=sys.stderr)
        for line in e.output.decode("utf8").split("\n"):
            print("[!!!]\t\t{}".format(line), file=sys.stderr)
        return {}
    search_matches = match_pattern.search(result)
    if search_matches:
        matches_dict = search_matches.groupdict()
        if "mdev" not in matches_dict:  # Windows
            matches_dict.update({"mdev": -1.0})
        return {k: float(v) for k, v in matches_dict.items()}
    else:
        return {"min": -1.0, "max": -1.0, "mdev": -1.0, "avg": -1.0}


def _windows(ip_address):
    pattern = re.compile(
        (rb'Minimum = (?P<min>[0-9]*)ms, '
         rb'Maximum = (?P<max>[0-9]*)ms, '
         rb'Average = (?P<avg>[0-9]*)ms')
    )
    return _run_ping(pattern, ["ping", "-n", "5", ip_address])


def _linux(ip_address, executable="ping"):
    pattern = re.compile(
        (rb'rtt min/avg/max/mdev = '
         rb'(?P<min>[0-9\.]*)/(?P<avg>[0-9\.]*)/'
         rb'(?P<max>[0-9\.]*)/(?P<mdev>[0-9\.]*) ms')
    )
    return _run_ping(pattern, [executable, "-c 5", "-n", "-q", ip_address])


def run(ip_address):
    """Ping an IP 5 times and return values based on the platform.

    Linux returns a dict with keys min, avg, max, mdev

    Keyword arguments:
    ip_address -- the target machine
    """
    result = {}
    if os.name == "posix":
        result = _linux(ip_address)
    elif os.name == "nt":
        result = _windows(ip_address)
    else:
        print("[!!!] Unknown os.name", file=sys.stderr)

    return result
