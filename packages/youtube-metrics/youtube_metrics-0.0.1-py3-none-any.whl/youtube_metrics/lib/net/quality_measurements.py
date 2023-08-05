"""Measure network quality to a server."""

import sys
import time

from geoip2.errors import GeoIP2Error
from geopy.distance import geodesic

from youtube_metrics.lib.net import dns, geo, local, ping, ping6

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
    ipv4_servers = dns.a_query(target)
    dns_a_time = time.time() - dns_a_start

    dns_aaaa_start = time.time()
    ipv6_servers = dns.aaaa_query(target)
    dns_aaaa_time = time.time() - dns_aaaa_start

    pings = []
    ping_start = time.time()
    for server in ipv4_servers:
        ping_result = ping.run(server)
        ping_result["ip"] = server
        pings.append(ping_result)
    ping_time = time.time() - ping_start

    ping6_start = time.time()
    for server in ipv6_servers:
        ping_result = ping6.run(server)
        ping_result["ip"] = server
        pings.append(ping_result)
    ping6_time = time.time() - ping6_start

    retval = {"pings": pings,
              "processing_time": {
                "dns_a_time": dns_a_time * 1000,
                "ping_time": ping_time * 1000,
                "dns_aaaa_time": dns_aaaa_time * 1000,
                "ping6_time": ping6_time * 1000}}
    return retval


def advanced(target):
    """Similar to basic but also measures destination to target IP addresses.

    Returns all measurements in a dictionary with keys "ping", "distances" and
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
                "long": result["longitude"]}

    my_coords = _lat_long(local.ip_address())
    target_ips = dns.a_query(target) + dns.aaaa_query(target)
    targets = {target_ip: _lat_long(target_ip) for target_ip in target_ips}
    distances = [{"ip": ip,
                  "coordinates": target,
                  "distance": int(geodesic(
                      (my_coords["lat"], my_coords["long"]),
                      (target["lat"], target["long"])).km)}
                 for ip, target in targets.items()]
    retval = basic(target)
    retval.update({"distances": distances})
    return retval
