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
