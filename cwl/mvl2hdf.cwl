#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: convert Doli .mvl to .hdf5 file (partial conversion of 15 metadata)

baseCommand: ["sh","script.sh"]

hints:
  DockerRequirement:
    dockerPull: python

inputs:
  in_file:
    type: File
    label: Doli binary file (.mvl) for tension-compression machine
    doc: |-
      vendor: Doli (www.doli.de)
      software: Version 2.0
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
          h5py
      # python script that does the work
      - entryname: convert.py
        entry: |-
          import struct, sys, os, hashlib
          import h5py                                    #CWL requirement
          import numpy as np
          from datetime import datetime

          convURI = 'https://raw.githubusercontent.com/NFDI4Chem/formaTAPIRest/main/cwl/mvl2hdf.cwl'
          convVersion = '1.0'

          ## COMMON PART FOR ALL CONVERTERS
          fileNameIn = '$(inputs.in_file.path)'
          fileNameOut= '$(inputs.out_file)'
          fIn   = open(fileNameIn,'br')
          fOut  = h5py.File(fileNameOut, 'w')
          metadata = fOut.create_group("metadata")
          converter = fOut.create_group("converter")
          converter.attrs['uri'] =     convURI
          converter.attrs['version'] = convVersion
          converter.attrs['original file name'] = fileNameIn
          md5Hash = hashlib.md5()
          md5Hash.update(fIn.read())
          converter.attrs['original md5-sum'] = md5Hash.hexdigest()

          def addAttrs(offset, format, hdfBranch, key):
            # helper function: add attribute to branch
            if type(key)==list:
              fIn.seek(key[0])
              key = bytearray(source=fIn.read(key[1])).decode('latin-1')
              key = key.replace('\\x00','')   # ValueError: VLEN strings do not support embedded NULLs
            fIn.seek(offset)
            if type(format)==int:
              value = bytearray(source=fIn.read(format)).decode('latin-1')
              if hdfBranch:
                hdfBranch.attrs[key] = value.replace('\\x00','')
            else:
              value = struct.unpack(format, fIn.read(struct.calcsize(format)))
              if hdfBranch:
                if len(value)==0:
                  hdfBranch.attrs[key] = value[0]
                else:
                  hdfBranch.attrs[key] = value
            return value

          def addData(format, hdfBranch, key, unit):
            # helper function: add data to branch
            data = fIn.read(struct.calcsize(format))
            if len(data) < struct.calcsize(format):
              return False
            data = struct.unpack(format, data)
            dset = hdfBranch.create_dataset(key, data=data)
            dset.attrs['unit'] = unit
            return True


          ## SPECIFIC TO THIS CONVERTER: METADATA
          n    = addAttrs(0x2c,   'i',  None, '')[0]                  # size of datasets
          addAttrs(       0x2B50, 'i',  metadata, 'number test')      # number of test
          date = addAttrs(0x2E3C, '6i', None, '')                     # date and time
          metadata.attrs['date'] = datetime(date[2],date[1],date[0],date[3],date[4],date[5]).isoformat()
          addAttrs(       0x529C,   64, metadata, 'name method')      # name of method
          # 0x6A20-0x6BD8: unclear
          addAttrs(       0x7DE4,   36, metadata, 'name folder')      # name of folder
          addAttrs(       0x7E09,   22, metadata, 'displacement cell')# displacement cell
          addAttrs(       0x7E21,   22, metadata, 'load cell')        # load cell
          for i in range(7):                                          # 7 key-value pairs
            addAttrs(0xA034+64*i,   64, metadata, [0xA674+32*i, 32])
          # 0x88A0: float : unclear
          addAttrs(       0xE29C,   36, metadata, 'file prefix')      # file-prefix
          addAttrs(       0xE450,   64, metadata, 'path')             # path

          ## SPECIFIC TO THIS CONVERTER: DATA
          fIn.seek(0x10ea0)
          addData(str(n)+'d', fOut, 'time',         's')
          addData(str(n)+'f', fOut, 'displacement', 'mm')
          addData(str(n)+'f', fOut, 'force',        'N')
          # last data
          # - unclear where existence and unit of this are stored
          # - this code: continue reading until failure
          idx = 0
          while True:
            idx += 1
            success = addData(str(n)+'f', fOut, 'data'+str(idx), '~')
            if not success:  #end of file
              break


          ## COMMON PART FOR ALL CONVERTERS
          fIn.close()
          fOut.close()


outputs:
  outfile:
    type: File
    label: custom HDF5 with k-series as well as metadata and converter groups
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
