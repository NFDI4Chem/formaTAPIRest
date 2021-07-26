#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
  in_file:
    type: File
  tmpdir:
      type: string
      default: "."
  dummyparameters:
    type: string[]
    default: []
  out_file: string

outputs:
  out_file:
    type: File
    format: edam:format_3245
    outputSource: convert/outfile

steps:
  unzip:
    run: unzip.cwl
    in:
      in_file: in_file
      out_dirname: tmpdir
    out: [out_dir]

  convert:
    run: bruker2jcamp.cwl
    in:
      in_dir: unzip/out_dir
      parameters: dummyparameters
      out_file: out_file
    out: [outfile]

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/
$schemas:
  - https://schema.org/version/latest/schemaorg-current-http.rdf
  - http://edamontology.org/EDAM_1.18.owl
