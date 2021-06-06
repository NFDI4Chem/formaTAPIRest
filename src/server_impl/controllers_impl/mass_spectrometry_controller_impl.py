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
from os import getenv
from os.path import basename
from pykube.config import KubeConfig
from pykube.http import HTTPClient
from pykube.objects import (Job, Pod)

## OpenAPI generated Code stuff
from openapi_server import util

import math

import tempfile
import os.path
import random
import string

from pathlib import Path

def mkdtempalpha(dir=None, prefix='') -> str:
    """Create a temporary directory name compatible with K8S pod naming conventions

    :param dir
    :type dir: str

    :param prefix
    :type prefix: str

    :rtype: str
    """

    if dir is None:
        dir = tempfile.gettempdir()

    while True:
        try:
            random_string = prefix \
                + ''.join(random.choices(string.ascii_lowercase, k=1)) \
                + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) \
                + ''.join(random.choices(string.ascii_lowercase, k=1))
            dirname = os.path.join(dir, random_string)
            Path(dirname).mkdir(parents=False, exist_ok=False)
        except FileExistsError as e:
            print(dirname + " already exists")
            continue
        break

    return dirname

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
#              "namespace": "chemotion", # "default",  # TODO this should be set
              "labels": {"app": k8s_job_name},
          },
      "spec": {
        "template": {
        "metadata": {
                "name": k8s_job_name,
#                "namespace": "chemotion", # "default",  # TODO this should be set from configs
                "labels": {"app": k8s_job_name},
            },
        "backoffLimit": "1",
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

def convert_pwi_zmz_xml2mz_ml(profile=None, inputfile=None):  # noqa: E501
    """Convert mzXML mass spectrometry raw data to mzML

    Uses Proteowizard MSConvert to convert an mzXML file into mzML # noqa: E501

    :param body:
    :type body: str

    :rtype: file
    """

    dockerimage = "chambm/pwiz-skyline-i-agree-to-the-vendor-licenses:latest"

    runner = "local" # Default
    if getenv("TAPIR_RUNNER") is not None:
        runner = getenv("TAPIR_RUNNER")

    if runner == "local":
        directory_name = mkdtempalpha(prefix="msconvert-")
        runcmd = ["msconvert"]
    elif runner == "docker":
        directory_name = mkdtempalpha(prefix="msconvert-")
        runcmd = [ "docker", "run", "--rm", \
                   "-v", directory_name+":"+directory_name, \
                   dockerimage, \
                   "wine", "msconvert"]
    elif runner == "kubernetes":
        directory_name = mkdtempalpha(dir="/data/", prefix="msconvert-")
        runcmd = ["wine", "msconvert"]
    else:
        print ("unknown runner")

    #infilename = directory_name+'/input.mzXML'
    infilename = directory_name+'/input.raw'
    outfilename = directory_name+'/output.mzML'
    jobid = basename(directory_name)

    cmd = runcmd + [ infilename, \
                "--outdir", directory_name, \
                "--outfile", "output.mzML"]

    try:
        inputfile.save(infilename)
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
            time.sleep(5)
            Job(pykube_api, k8s_job_obj).create()
            print ("submitted", file=sys.stderr)

            wait_for_job(pykube_api, jobid)
            print ("finished", file=sys.stderr)

            Job(pykube_api, k8s_job_obj).delete()
            time.sleep(5)
            print ("deleted", file=sys.stderr)

        with open(outfilename, 'rb') as outfile:
            data = outfile.read()
            time.sleep(5)

    finally:
        print ("not deleting workdir", file=sys.stderr)
        #shutil.rmtree(directory_name, ignore_errors=True)

    return data


def wait_for_job(pykube_api, job_id):
    """Checks the state of a job already submitted on k8s."""

    succeeded = 0
    active = 0
    failed = 0

    #print (Job(pykube_api, jobs.response['items'][0]), file=sys.stderr)

    jobs = Job.objects(pykube_api).filter(selector="app=" + job_id)
    if len(jobs.response['items']) == 1:
        iteration = 1
        while True:
            time.sleep(math.log2(iteration+1))
            iteration += 1
            jobs = Job.objects(pykube_api).filter(selector="app=" + job_id)
            if len(jobs.response['items']) < 1:
                continue

            job = Job(pykube_api, jobs.response['items'][0])

            if 'succeeded' in job.obj['status']:
                succeeded = job.obj['status']['succeeded']
            if 'active' in job.obj['status']:
                active = job.obj['status']['active']
            if 'failed' in job.obj['status']:
                failed = job.obj['status']['failed']

            print ("succeeded: ", succeeded, ", active: ", active, "failed: ", failed, file=sys.stderr)

            # This assumes jobs dependent on a single pod, single container
            if succeeded > 0:
                print ("exit succeeded", file=sys.stderr)
                return True
            elif failed > 0 :
                print ("exit failed", file=sys.stderr)
                return False
            elif active > 0 and failed <= 2:
                print ("keep trying", file=sys.stderr)
                continue
            elif failed > 2:
                print ("exit failed", file=sys.stderr)
                return False
