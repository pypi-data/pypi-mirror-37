"""Wrapper for geoip2 Geolite2 database."""

import geoip2.database
import pkg_resources


class GeoIP2:
    database = pkg_resources.resource_filename(
        __name__, "data/GeoLite2-City/GeoLite2-City.mmdb")

    def __init__(self):
        self.reader = geoip2.database.Reader(self.database)

    def __del__(self):
        self.reader.close()

    def lookup(self, ip_address):
        """Lookup an IP

        Keyword arguments:
        ip_address -- target
        """
        match = {}
        resp = self.reader.city(ip_address)
        match = {"country": resp.country.iso_code,
                 "city": resp.city.name,
                 "latitude": resp.location.latitude,
                 "longitude": resp.location.longitude}
        return match
