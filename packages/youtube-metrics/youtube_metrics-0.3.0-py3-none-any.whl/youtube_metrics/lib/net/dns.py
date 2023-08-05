"""Singleton DNS wrapper for dnspython."""

from dns import resolver as dns_resolver
from dns.exception import DNSException


class Resolver:
    """
    Singleton class for dns_resolver.

    We do it like this so we can change the nameservers at will
    """

    _singleton = None

    class _resolver:
        def __init__(self):
            self.resolver = dns_resolver.Resolver()

        def resolve(self, domain, query):
            """
            Run a DNS resolve using a Singleton instance of dnspython resolver.

            Keyword arguments
            domain -- target URL
            query -- DNS query type (e.g. "A" or "AAAA")
            """
            try:
                return [a_record.to_text()
                        for a_record in self.resolver.query(domain, query)]
            except DNSException:
                return []

    @classmethod
    def resolve(cls, domain, query, nameservers=None):
        """Run a DNS resolve using a Singleton instance of dnspython resolver.

        Keyword arguments
        domain -- target URL
        query -- DNS query type (e.g. "A" or "AAAA")
        nameservers -- a list of nameservers.
                       Defaults to ["1.1.1.1", "1.0.0.1"]
        """
        if cls._singleton is None:
            cls._singleton = cls._resolver()

        cls._singleton.resolver.nameservers = (nameservers or
                                               ["1.1.1.1", "1.0.0.1"])
        return cls._singleton.resolve(domain, query)


def a_query(domain, nameservers=None):
    """Run DNS A query.

    Keyword arguments:
    domain -- target URL
    nameservers -- a list of nameservers. Defaults to ["1.1.1.1", "1.0.0.1"]
    """
    return Resolver.resolve(domain, "A", nameservers)


def aaaa_query(domain, nameservers=None):
    """Run DNS AAAA query.

    Keyword arguments:
    domain -- target URL
    nameservers -- a list of nameservers. Defaults to ["1.1.1.1", "1.0.0.1"]
    """
    return Resolver.resolve(domain, "AAAA", nameservers)
