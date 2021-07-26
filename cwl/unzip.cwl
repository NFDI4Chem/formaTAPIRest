#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Extract the entire content of a file

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - '$({class: "Directory", basename: inputs.out_dirname, listing: []})'

baseCommand: ["unzip", "-x", "-d"]
inputs:
  in_file:
    type: File
    label: ZIP file
    inputBinding:
      position: 4
  out_dirname:
    type: string
    inputBinding:
      position: 3

outputs:
  out_dir:
    type: Directory
    label: Directory with extracted files
    outputBinding:
      glob: "$(inputs.out_dirname)/*"

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0002-7899-7192
    s:email: mailto:sneumann@ipb-halle.de
    s:name: Steffen Neumann
