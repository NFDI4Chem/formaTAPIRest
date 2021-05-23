import connexion
import six
import subprocess

from openapi_server import util


def convert_pwi_zmz_xml2mz_ml(body=None):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    with open('/tmp/input.mzData', 'wb') as infile:
        infile.write(body)

    subprocess.call(["/usr/bin/msconvert", \
                    "/tmp/input.mzData", \
                    "--outdir", "/tmp", \
                    "--outfile", "output.mzML"], \
                    shell=False)

    with open('/tmp/output.mzML', 'rb') as outfile:
        data = outfile.read()

    return data
