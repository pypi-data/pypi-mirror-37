"""Implements converters for data."""
import csv
from io import StringIO

FIELDS = ['me.ip', 'me.coords.lat', 'me.coords.lon', 'video.metadata.id',
          'video.metadata.uploader', 'video.metadata.title',
          'video.metadata.duration', 'video.metadata.webpage_url',
          'video.metadata.view_count', 'video.metadata.url',
          'video.metadata.ext', 'video.metadata.height',
          'video.metadata.format_note', 'video.metadata.filesize',
          'video.metadata.width', 'video.metadata.error',
          'video.statistics.cache_url', 'video.statistics.ping.min',
          'video.statistics.ping.avg', 'video.statistics.ping.max',
          'video.statistics.ping.mdev', 'video.statistics.ping.ip',
          'video.statistics.processing_time.dns_time',
          'video.statistics.processing_time.ping_time',
          'video.statistics.distance.ip',
          'video.statistics.distance.coordinates.lat',
          'video.statistics.distance.coordinates.lon',
          'video.statistics.distance.distance',
          'video.statistics.download.downloaded',
          'video.statistics.download.throughput',
          'video.statistics.download.processing_time.request_time',
          'video.statistics.download.processing_time.response_time',
          'video.statistics.download.format']


def _flatten_dict(parent_key, _dict):
    new_dict = {}
    for k, v in _dict.items():
        if parent_key:
            k = "{}.{}".format(parent_key, k)
        if isinstance(v, dict):
            new_dict.update(_flatten_dict(k, v))
        else:
            new_dict[k] = v

    return new_dict


def dict_to_csv(payload):
    csv_string = StringIO()
    writer = csv.DictWriter(csv_string, fieldnames=FIELDS)
    writer.writeheader()
    flattened = []
    for _dict in payload:
        flattened.append(_flatten_dict("", _dict))
    writer.writerows(flattened)
    return csv_string.getvalue()
