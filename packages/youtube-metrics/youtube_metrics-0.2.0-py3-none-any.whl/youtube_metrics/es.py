import sys

import pkg_resources


def main(args):
    template = pkg_resources.resource_string(
        __name__, "data/elasticsearch_template.json")
    print(template.decode("utf8"))
    sys.exit(0)
