#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: Extract the entire content of a ZIP archive

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
    format: edam:format_3987
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
    format: edam:format_1915c
    outputBinding:
      glob: "$(inputs.out_dirname)/*"

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
