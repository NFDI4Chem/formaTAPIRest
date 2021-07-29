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

# List of converters
| file name               | label                                                                  | input                            | output            | author             |
|:------------------------|:-----------------------------------------------------------------------|:---------------------------------|:------------------|:-------------------|
| png2jpg.cwl             | Convert png to jpg image                                               | edam:format_3603                 | edam:format_3579  | Steffen Brinckmann |
| osc2hdf.cwl             | convent osc file to hdf5 file                                          | edam:format_2330                 | edam:format_3590  | Steffen Brinckmann |
| msconvert.cwl           | Uses Proteowizard MSConvert to convert vendor files into mzML          | edam:format_3245                 | edam:format_3244  | Steffen Neumann    |
| libremsconvert.cwl      | Uses Proteowizard MSConvert to convert an mzXML file into mzML         | edam:format_3654                 | edam:format_3244  | Steffen Neumann    |
| zip.cwl                 | ZIP an entire directory                                                | edam:format_1915                 | edam:format_3987  | Steffen Neumann    |
| unzip.cwl               | Extract the entire content of a ZIP archive                            | edam:format_3987                 | edam:format_1915c | Steffen Neumann    |
| zipped2bruker2jcamp.cwl | Uses Bruker TopSpin to convert a zipped NMR data directory to JCAMP-DX | Zipped Bruker NMR data directory | edam:format_3245  | Steffen Neumann    |
| bruker2jcamp.cwl        | Uses Bruker TopSpin to convert NMR data to JCAMP-DX                    | Bruker NMR data directory        | edam:format_3245  | Steffen Neumann    |
| md5sum.cwl              | Dummy test (calculate md5sum) of input->output conversion              | edam:format_1915                 | ncit:NCIT_C171276 | Steffen Brinckmann |