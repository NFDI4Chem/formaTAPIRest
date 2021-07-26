#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Uses Bruker TopSpin to convert NMR data to JCAMP-DX

requirements:
  InitialWorkDirRequirement:
    listing:
      - entry: $(inputs.in_dir)
        writable: true

baseCommand: myjcampdx.sh

hints:
  DockerRequirement:
    dockerImageId: nfdi4chem/topspin:4.1.1.2-0.1

inputs:
  in_dir:
    type: Directory
    label: Bruker NMR data directory
    doc: |-
      vendor: Bruker
      instrument: NMR
    inputBinding:
        position: 1
  parameters:
    type: string[]
    inputBinding:
      position: 3
  out_file:
    type: string
    inputBinding:
      position: 2

outputs:
  outfile:
    type: File
    label: JCAMP-DX spectrum
    format: edam:format_3245
    outputBinding:
      glob: $(inputs.out_file)

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
