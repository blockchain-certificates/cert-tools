import base64
import json
import os
import sys
from datetime import datetime, timezone

import configargparse
import pytz

if sys.version > '3':
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))
png_prefix = 'data:image/png;base64,'
URN_UUID_PREFIX = 'urn:uuid:'


def make_action(additional_arg):
    class customAction(configargparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            json_obj = json.loads(values)['fields']
            setattr(args, self.dest, json_obj)

    return customAction


def encode_image(filename):
    with open(filename, "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        png_str = png_prefix + encoded.decode('utf-8')
        return png_str


def urljoin_wrapper(part1, part2):
    return urljoin(part1, part2)


def encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def create_iso8601_tz():
    ret = datetime.now(timezone.utc)
    return ret.isoformat()