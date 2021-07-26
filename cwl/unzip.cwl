#/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - '$({class: "Directory", basename: inputs.out_dirname, listing: []})'

baseCommand: ["unzip", "-x", "-d"]
inputs:
  in_file:
    type: File
    inputBinding:
      position: 4
  out_dirname:
    type: string
    inputBinding:
      position: 3

outputs:
  out_dir:
    type: Directory
    outputBinding:
      glob: "$(inputs.out_dirname)/*"
