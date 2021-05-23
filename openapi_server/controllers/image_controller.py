import connexion
import six
import subprocess

from openapi_server import util


def convert_image_png2_jpg(body=None):  # noqa: E501
    """Convert a JPG image to PNG

    Uses ImageMagick to convert a JPG image to PNG # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    with open('/tmp/input.png', 'wb') as infile:
        infile.write(body)

    subprocess.call(["/usr/bin/convert", "/tmp/input.png", "/tmp/output.jpg"], shell=False)

    with open('/tmp/output.jpg', 'rb') as outfile:
        data = outfile.read()

    return data
