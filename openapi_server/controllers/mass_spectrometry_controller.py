import connexion
import six
import subprocess

from openapi_server import util


def convert_pwi_zmz_data2mz_ml(body=None):  # noqa: E501
    """Convert a JPG image to PNG

    Uses ImageMagick to convert a JPG image to PNG # noqa: E501

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
