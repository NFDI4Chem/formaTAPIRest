# TAPIR | formaTAPIRest
## How to use:
1. create a YML file (e.g. "default.yml") with:
    - conversion file "./test.cwl"
    - input file "./EBSD.osc"
    - output file "output.hdf5"
    ```yml
    cwl:tool: ./test.cwl
    in_file:
      class: File
      path: ./input.dat
    out_file: output.hdf5
    ```
1. run the conversion with
```sh
cwl-runner default.yml
```
If conversion uses docker, you should run the command with 'sudo'

## Add parameters into your .yml file
```yml
parameters: [--text, --tag]
```

### Example: md5sum test
```yml
cwl:tool: ./md5sum.cwl
in_file:
  class: File
  format: http://edamontology.org/format_3603
  path: kitten.png
parameters: [--text, --tag]
out_file: myOutput.txt
```

## Notes for developers of cwl-files
### Rules
Files must have the following content, which is partly checked by produceTable.py:
- a top-level label is required
- author information (name and orcid-link)
- input files require a label and optionally a doc-string
- output files require EDAM classification and  a label

### Examples for conversion
- based on a command: png2jpg.cwl
- multiple steps: zipped2bruker2jcamp.yml
- use docker image: msconvert.yml
- use python with specific dependencies (incl. pull python-docker): osc2hdf.yml

## List of converters
