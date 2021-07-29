#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Convert png to jpg image

baseCommand: convert

inputs:
  in_file:
    type: File
    label: png file format
    doc: |-
       vendor: Internet Engineering Task Force
       instrument:
    format: edam:format_3603
    inputBinding:
      position: 2
  parameters:
    type: string[]
    inputBinding:
      position: 1
  out_file:
    type: string
    inputBinding:
      position: 3

outputs:
  outfile:
    type: File
    outputBinding:
      glob: $(inputs.out_file)

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0003-0930-082X
    s:name: Steffen Brinckmann

s:citation: https://dx.doi.org/10.6084/m9.figshare.3115156.v2
s:codeRepository: https://github.com/common-workflow-language/common-workflow-language
s:dateCreated: "2021-6-14"
s:license: https://spdx.org/licenses/MIT

$namespaces:
  s: https://schema.org/
  edam: http://edamontology.org/
$schemas:
  - https://schema.org/version/latest/schemaorg-current-http.rdf
  - http://edamontology.org/EDAM_1.18.owl
