import connexion
import six
import subprocess
import tempfile
import sys
import shutil
import time

## For K8S jobs
import pykube
from os import environ as os_environ
from os.path import basename
from pykube.config import KubeConfig
from pykube.http import HTTPClient
from pykube.objects import (Job, Pod)

## OpenAPI generated Code stuff
from openapi_server import util

def create_k8s_job_obj(k8s_job_name=None, dockerimage=None, cmd=None):
    """Create a job definition

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param k8s_job_name:
    :type k8s_job_name: str

    :param dockerimage:
    :type dockerimage: str

    :param cmd:
    :type cmd: List

    :rtype: Dict
    """

    k8s_job_obj = {
      "apiVersion": "batch/v1", #runner_param_specs['k8s_job_api_version'],
      "kind": "Job",
      "metadata": {
              # metadata.name is the name of the pod resource created, and must be unique
              # http://kubernetes.io/docs/user-guide/configuring-containers/
              "name": k8s_job_name,
              "namespace": "chemotion", # "default",  # TODO this should be set
              "labels": {"app": k8s_job_name},
          },
      "spec": {
        "template": {
        "metadata": {
                "name": k8s_job_name,
                "namespace": "chemotion", # "default",  # TODO this should be set from configs
                "labels": {"app": k8s_job_name},
            },
        "spec": {
          "containers": [{
              "name": "c",
              "image": dockerimage,
              "command": cmd,
              "volumeMounts": [{
              "name": "conversion",
              "mountPath": "/data"
              }]
          }],
          "volumes":[{
            "name": "conversion",
            "persistentVolumeClaim": {
                "claimName": "pvc-conversion"
            }
          }],
          "restartPolicy": "Never"
         }
        }
      }
    }
    return k8s_job_obj

def convert_pwi_zmz_xml2mz_ml_impl(body=None, runner="local"):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    dockerimage = "chambm/pwiz-skyline-i-agree-to-the-vendor-licenses:latest"

    if runner == "local":
        directory_name = tempfile.mkdtemp(prefix="msconvert-")
        runcmd = ["msconvert"]
    elif runner == "docker":
        directory_name = tempfile.mkdtemp(dir="/data/", prefix="msconvert-")
        runcmd = [ "docker", "run", "--rm", \
                   "-v", directory_name+":"+directory_name, \
                   dockerimage, \
                   "wine", "msconvert"]
    elif runner == "kubernetes":
        directory_name = tempfile.mkdtemp(dir="/data/", prefix="msconvert-")
        runcmd = ["wine", "msconvert"]
    else:
        print ("unknown runner")

    infilename = directory_name+'/input.mzXML'
    outfilename = directory_name+'/output.mzML'
    jobid = basename(directory_name)

    cmd = runcmd + [ infilename, \
                "--outdir", directory_name, \
                "--outfile", "output.mzML"]

    try:
        with open(infilename, 'wb') as infile:
            infile.write(body)

            if runner == "local" or runner == "docker":
                print (cmd, file=sys.stderr)
                subprocess.call(cmd, shell=False)
            elif runner == "kubernetes":
                # This creates the PyKube configuration from ~/.kube/config
                # pykube_api = HTTPClient(KubeConfig.from_file())

                # This creates the PyKube configuration if run from inside a Pod
                pykube_api = HTTPClient(KubeConfig.from_service_account())
                k8s_job_obj = create_k8s_job_obj(jobid, dockerimage, cmd)

                # Actually create that job
                Job(pykube_api, k8s_job_obj).create()

                time.sleep(60) # "Wait" until job shall be finished

        with open(outfilename, 'rb') as outfile:
            data = outfile.read()
    finally:
        shutil.rmtree(directory_name, ignore_errors=True)

    return data
