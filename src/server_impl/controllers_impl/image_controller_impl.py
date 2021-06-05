import connexion
import six
import subprocess
import tempfile
import sys
import shutil

from openapi_server import util


def convert_image_png2_jpg(body=None):  # noqa: E501
    """Convert a JPG image to PNG

    Uses ImageMagick to convert a JPG image to PNG # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    try:
        directory_name = tempfile.mkdtemp()
        infilename = directory_name+'/input.png'
        outfilename = directory_name+'/output.jpg'
        with open(infilename, 'wb') as infile:
            infile.write(body)

            cmd = ["/usr/bin/convert", infilename, outfilename]
            print (cmd, file=sys.stderr)
            subprocess.call(cmd, shell=False)

        with open(outfilename, 'rb') as outfile:
            data = outfile.read()
    finally:
        shutil.rmtree(directory_name, ignore_errors=True)

    return data
