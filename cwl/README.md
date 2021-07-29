# Examples
Put the yml code into default.yml and run it with
```sh
cwl-runner default.yml
```

## Example: md5sum test
```yml
cwl:tool: ./md5sum.cwl
in_file:
  class: File
  format: http://edamontology.org/format_3603
  path: kitten.png
parameters: [--text, --tag]
out_file: myOutput.txt
```

## Example: png2jpg conversion
```yml
cwl:tool: ./png2jpg.cwl
in_file:
  class: File
  format: http://edamontology.org/format_3603
  path: kitten.png
parameters: []
out_file: myPic.jpg
```

## Example: mzXML2mzML conversion
```yml
cwl:tool: ./libremsconvert.cwl
in_file:
  class: File
  format: edam:format_3654
  path: RtmpIX4kGntest_write.mzXML
parameters: []
```

## Example: RAW2mzML conversion
```yml
cwl:tool: ./msconvert.cwl
in_file:
  class: File
  format: edam:format_3712
  path: /tmp/nuts/fa3.RAW
parameters: []
```

# Notes for developers of cwl-files

## Rules
Files must have the following content, which is partly checked by produceTable.py:
- a top-level label is required
- author information (name and orcid-link)
- input files require a label and optionally a doc-string
- output files require EDAM classification and  a label

## Examples for conversion
- based on a command: png2jpg.cwl
- multiple steps: zipped2bruker2jcamp.yml
- use docker image: msconvert.yml
- use python with specific dependencies (incl. pull python-docker): osc2hdf.yml

# List of converters
| file name               | label                                                                  | input                                  | output            | author             |
|:------------------------|:-----------------------------------------------------------------------|:---------------------------------------|:------------------|:-------------------|
| bruker2jcamp.cwl        | Uses Bruker TopSpin to convert NMR data to JCAMP-DX                    | Bruker NMR data directory              | edam:format_3245  | Steffen Neumann    |
| msconvert.cwl           | Uses Proteowizard MSConvert to convert vendor files into mzML          | edam:format_3245                       | edam:format_3244  | Steffen Neumann    |
| zipped2bruker2jcamp.cwl | Uses Bruker TopSpin to convert a zipped NMR data directory to JCAMP-DX | Zipped Bruker NMR data directory       | edam:format_3245  | Steffen Neumann    |
| libremsconvert.cwl      | Uses Proteowizard MSConvert to convert an mzXML file into mzML         | edam:format_3654                       | edam:format_3244  | Steffen Neumann    |
| osc2hdf.cwl             | convent osc file to hdf5 file (partial conversion)                     | EDAX binary file (.osc) with EBSD data | edam:format_3590  | Steffen Brinckmann |
| md5sum.cwl              | Test (calculate md5sum) of input->output conversion                    | edam:format_1915                       | ncit:NCIT_C171276 | Steffen Brinckmann |
| unzip.cwl               | Extract the entire content of a ZIP archive                            | edam:format_3987                       | edam:format_1915c | Steffen Neumann    |
| png2jpg.cwl             | Convert png to jpg image                                               | edam:format_3603                       | edam:format_3579  | Steffen Brinckmann |