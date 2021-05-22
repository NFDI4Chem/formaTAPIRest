import connexion
import six

from openapi_server import util


def convert_image_png2_jpg(body=None):  # noqa: E501
    """Convert a JPG image to PNG

    Uses ImageMagick to convert a JPG image to PNG # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """
    with open('/tmp/kitten.png', 'rb') as outfile:
        data = outfile.read() #we are assigning a variable which will read whatever in the file and it will be stored in the variable called data.

    return data
