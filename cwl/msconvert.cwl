#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Uses Proteowizard MSConvert to convert vendor files into mzML

baseCommand: ["wine", "msconvert"]
hints:
  DockerRequirement:
    dockerPull: chambm/pwiz-skyline-i-agree-to-the-vendor-licenses

inputs:
  in_file:
    type: File
    label: mzXML or vendor file format
    format: edam:format_3245
    inputBinding:
      position: 1
  parameters:
    type: string[]
    inputBinding:
      position: 2


outputs:
  outfile:
    type: File
    label: mzML file
    format: edam:format_3244
    outputBinding:
      glob: "*.mzML"

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0002-7899-7192
    s:email: mailto:sneumann@ipb-halle.de
    s:name: Steffen Neumann

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
