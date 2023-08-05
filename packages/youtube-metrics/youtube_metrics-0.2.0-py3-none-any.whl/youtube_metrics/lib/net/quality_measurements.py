"""Measure network quality to a server."""

import sys
import time

from geoip2.errors import GeoIP2Error
from geopy.distance import geodesic

from youtube_metrics.lib.net import dns, geo, local, ping

GEOIP2 = geo.GeoIP2()


def basic(target):
    """Run DNS and ping the target IP-addresses.

    Returns all measurements in a dictionary with keys "ping" and
    "processing_time".

    ping times are in milliseconds

    processing times are in milliseconds

    Keyword arguments
    target -- URL of the target server
    """
    dns_a_start = time.time()
    server = dns.a_query(target)[0]
    dns_a_time = time.time() - dns_a_start

    ping_start = time.time()
    ping_result = ping.run(server)
    ping_result["ip"] = server
    ping_time = time.time() - ping_start

    retval = {"ping": ping_result,
              "processing_time": {
                  "dns_time": dns_a_time * 1000,
                  "ping_time": ping_time * 1000}}
    return retval


def advanced(target):
    """Similar to basic but also measures destination to target IP addresses.

    Returns all measurements in a dictionary with keys "ping", "distance" and
    "processing_time".

    Distances are in kilometers.

    Keyword Arguments:
    target -- target URL
    """
    def _lat_long(target):
        try:
            result = GEOIP2.lookup(target)
        except GeoIP2Error as e:
            print("[!!!] GeoIP2 error: {}".format(e), file=sys.stderr)
            raise e
        return {"lat": result["latitude"],
                "lon": result["longitude"]}

    my_coords = _lat_long(local.ip_address())
    target_ip = dns.a_query(target)[0]
    target_coords = _lat_long(target_ip)
    distance = {"ip": target_ip,
                "coordinates": target_coords,
                "distance": int(geodesic(
                    (my_coords["lat"], my_coords["lon"]),
                    (target_coords["lat"], target_coords["lon"])).km)}
    retval = basic(target)
    retval.update({"distance": distance})
    return retval
