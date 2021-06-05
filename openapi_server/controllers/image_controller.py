import connexion
import six

from openapi_server import util

import openapi_server.server_impl.controllers_impl.image_controller_impl as ImageController_impl

#from openapi_server.server_impl.controllers_impl.image_controller_impl import ImageController_impl

def convert_image_png2_jpg(body=None):  # noqa: E501
    """Convert a JPG image to PNG

    Uses ImageMagick to convert a JPG image to PNG # noqa: E501

    :param body: 
    :type body: str

    :rtype: file
    """
    return ImageController_impl.convert_image_png2_jpg(body)  # noqa: E501
