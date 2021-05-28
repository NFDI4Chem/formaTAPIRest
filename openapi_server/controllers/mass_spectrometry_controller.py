import connexion
import six

## OpenAPI generated Code stuff
from openapi_server import util
from openapi_server.controllers.mass_spectrometry_controller_impl import convert_pwi_zmz_xml2mz_ml_impl

def convert_pwi_zmz_xml2mz_ml(body=None):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    return convert_pwi_zmz_xml2mz_ml_impl(body, runner="local")
