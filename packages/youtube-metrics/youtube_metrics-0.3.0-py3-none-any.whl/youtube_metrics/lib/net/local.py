"""Local network utilities."""

import requests


def ip_address():
    """Connect to stat.ripe.net and return this machine's local IP."""
    return (requests
            .get("https://stat.ripe.net/data/whats-my-ip/data.json")
            .json()["data"]["ip"])
