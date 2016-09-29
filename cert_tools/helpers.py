import base64
import os
import sys


if sys.version > '3':
    from urllib.parse import urljoin
else:
    from urlparse import urljoin


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))
png_prefix = 'data:image/png;base64,'


def encode_image(filename):
    with open(filename, "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        png_str = png_prefix + encoded.decode('utf-8')
        return png_str


def urljoin_wrapper(part1, part2):
    return urljoin(part1, part2)


def normalize_data_path(*argv):
    if os.path.isabs(argv[0]):
        return os.path.join(*argv)
    return os.path.join(PROJECT_ROOT, *argv)