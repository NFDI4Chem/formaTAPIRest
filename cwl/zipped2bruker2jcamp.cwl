#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
label: Uses Bruker TopSpin to convert a zipped NMR data directory to JCAMP-DX

inputs:
  in_file:
    type: File
    label: Zipped Bruker NMR data directory
  tmpdir:
      type: string
      default: "."
  dummyparameters:
    type: string[]
    default: []
  out_file: string

outputs:
  outfile:
    type: File
    label: JCAMP-DX spectrum file
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

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0002-7899-7192
    s:email: mailto:sneumann@ipb-halle.de
    s:name: Steffen Neumann

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/
$schemas:
  - https://schema.org/version/latest/schemaorg-current-http.rdf
  - http://edamontology.org/EDAM_1.18.owl
