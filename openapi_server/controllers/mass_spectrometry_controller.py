import connexion
import six

from openapi_server import util

import openapi_server.server_impl.controllers_impl.mass_spectrometry_controller_impl as MassSpectrometryController_impl

#from openapi_server.server_impl.controllers_impl.mass_spectrometry_controller_impl import MassSpectrometryController_impl

def convert_pwi_zmz_xml2mz_ml(profile=None, inputfile=None):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param profile: 
    :type profile: str
    :param inputfile: 
    :type inputfile: str

    :rtype: file
    """
    return MassSpectrometryController_impl.convert_pwi_zmz_xml2mz_ml(profile, inputfile)  # noqa: E501
