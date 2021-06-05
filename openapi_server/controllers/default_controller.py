import connexion
import six

from openapi_server import util

import openapi_server.server_impl.controllers_impl.default_controller_impl as DefaultController_impl

#from openapi_server.server_impl.controllers_impl.default_controller_impl import DefaultController_impl

def list_get():  # noqa: E501
    """Get list of all convertes and their possible targets

     # noqa: E501


    :rtype: str
    """
    return DefaultController_impl.list_get()  # noqa: E501

import openapi_server.server_impl.controllers_impl.default_controller_impl as DefaultController_impl

#from openapi_server.server_impl.controllers_impl.default_controller_impl import DefaultController_impl

def ping_get():  # noqa: E501
    """Check if server alive

     # noqa: E501


    :rtype: None
    """
    return DefaultController_impl.ping_get()  # noqa: E501
