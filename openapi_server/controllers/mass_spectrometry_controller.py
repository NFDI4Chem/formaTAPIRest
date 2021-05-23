import connexion
import six
import subprocess
import tempfile
import sys
import shutil

from openapi_server import util


def convert_pwi_zmz_xml2mz_ml(body=None):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    try:
        directory_name = tempfile.mkdtemp()
        infilename = directory_name+'/input.mzXML'
        outfilename = directory_name+'/output.mzML'
        with open(infilename, 'wb') as infile:
            infile.write(body)

            cmd = ["/usr/bin/msconvert", \
                    infilename, \
                    "--outdir", directory_name, \
                    "--outfile", "output.mzML"]
            print (cmd, file=sys.stderr)
            subprocess.call(cmd, shell=False)

        with open(outfilename, 'rb') as outfile:
            data = outfile.read()
    finally:
        shutil.rmtree(directory_name, ignore_errors=True)

    return data
