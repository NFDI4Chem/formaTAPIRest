#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: convent osc file to hdf5 file (partial conversion)

baseCommand: ["sh","script.sh"]

hints:
  DockerRequirement:
    dockerPull: python

inputs:
  in_file:
    type: File
    label: EDAX binary file (.osc) with EBSD data
    doc: |-
      vendor: EDAX Ametek
      software: old OIM versions
  out_file:
    type: string

requirements:
  InitialWorkDirRequirement:
    listing:
      # main shell script that starts pip and python
      - entryname: script.sh
        entry: |-
          pip3 install -r requirements.txt
          python convert.py
      # pip install packages
      - entryname: requirements.txt
        entry: |-
          orix
      # python script that does the work
      - entryname: convert.py
        entry: |-
          import math, h5py, sys, os, hashlib
          import numpy as np
          from diffpy.structure import Structure
          from orix.io import load, save                      #CWL requirement
          from orix.crystal_map import CrystalMap, PhaseList
          from orix.quaternion.rotation import Rotation

          convURI = 'https://raw.githubusercontent.com/NFDI4Chem/formaTAPIRest/main/cwl/osc2hdf.cwl'
          convVersion = '1.0'

          fileNameIn = '$(inputs.in_file.path)'
          fileNameOut= '$(inputs.out_file)'
          f = open(fileNameIn,"r")

          def find_subsequence(seq, subseq):
            target = np.dot(subseq, subseq)
            candidates = np.where(np.correlate(seq, subseq, mode='valid') == target)[0]
            # some of the candidates entries may be false positives, double check
            check = candidates[:, np.newaxis] + np.arange(len(subseq))
            mask = np.all((np.take(seq, check) == subseq), axis=-1)
            return candidates[mask]

          header = np.fromfile(f, dtype=np.uint32, count=8)
          n = header[6]   #number of data points
          #header[4]: numPixelX; header[5]: numPixelY
          numPhases = header[1]

          # find start position by using startByte-pattern
          bufferLength = int(math.pow(2,20))
          startBytes = np.array( [ int(i,16)  for i in ['B9', '0B', 'EF', 'FF', '02', '00', '00', '00'] ],dtype=np.uint8 )
          startPos = 0
          f.seek(startPos)
          startData = np.fromfile(f, dtype=np.uint8, count=bufferLength)
          # startPos += [x for x in xrange(len(startData)-len(startBytes)) if (startData[x:x+len(startBytes)] == startBytes).all() ][0]
          startPos += find_subsequence( startData, startBytes)[0]
          f.seek(startPos+8)

          # there are different osc file versions, one does have some count of data, the other proceeds with xStep and yStep (!=1)
          dn = np.double( np.fromfile(f,dtype=np.uint32, count=1))
          if round(((dn/4-2)/10)/n) != 1:
            f.seek(startPos+8)
          stepSizeX = np.double(np.fromfile(f, dtype=np.float32, count=1))
          stepSizeY = np.double(np.fromfile(f, dtype=np.float32, count=1))

          data = np.reshape( np.double(np.fromfile(f, count=n*10, dtype=np.float32)) , (n,10) )
          phi1    = data[:,0].astype(np.float16)
          PHI     = data[:,1].astype(np.float16)
          phi2    = data[:,2].astype(np.float16)
          x       = data[:,3].astype(np.float32)
          y       = data[:,4].astype(np.float32)
          IQ      = data[:,5].astype(np.float16)
          CI      = data[:,6].astype(np.float16)
          phaseID = data[:,7].astype(np.float16) + 1
          SEMsignal= data[:,8].astype(np.float16) #SEMSignal
          fit     = data[:,9].astype(np.float16) #Fit

          numPhases = len(np.unique(phaseID))
          structures, names = [], []
          for i in range(numPhases):
            structures.append(Structure(title='phase'+str(i)))
            names.append('phase'+str(i))
          phaseList = PhaseList(names=names, point_groups=[None]*numPhases, structures=structures)

          #Assemble new data set
          eulerAngles = np.column_stack((phi1, PHI, phi2))
          rotations = Rotation.from_euler(eulerAngles)
          properties = {"iq":IQ, "ci":CI, 'sem':SEMsignal, 'fit':fit}
          ebsd2 = CrystalMap(rotations=rotations,
                          phase_id=phaseID,x=x, y=y,
                          phase_list=phaseList, prop=properties)

          #some corrections
          ebsd2.scan_unit = "um"
          save(filename=fileNameOut, object2write=ebsd2)
          f.close()

          #add converter information
          fIn   = open(fileNameIn,'br')
          fOut  = h5py.File(fileNameOut, 'a')
          converter = fOut.create_group("converter")
          converter.attrs['uri'] =     convURI
          converter.attrs['version'] = convVersion
          converter.attrs['original file name'] = fileNameIn
          md5Hash = hashlib.md5()
          md5Hash.update(fIn.read())
          converter.attrs['original md5-sum'] = md5Hash.hexdigest()
          fIn.close()
          fOut.close()

outputs:
  outfile:
    type: File
    label: orix HDF5 file (pypi.org/project/orix)
    format: edam:format_3590
    outputBinding:
      glob: $(inputs.out_file)

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0003-0930-082X
    s:name: Steffen Brinckmann

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/
$schemas:
  - https://schema.org/version/latest/schemaorg-current-http.rdf
  - http://edamontology.org/EDAM_1.18.owl
