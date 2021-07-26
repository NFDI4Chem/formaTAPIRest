# Examples
Put the yml code into default.yml and run it with
```sh
cwl-runner default.yml
```

## Example: dummy test
```yml
cwl:tool: ./dummy.cwl
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
| file name           | label                                                          | input                       | output                                        | author             |
|:--------------------|:---------------------------------------------------------------|:----------------------------|:----------------------------------------------|:-------------------|
| dummy.cwl           | Dummy test (calculate md5sum) of input->output conversion      | any file format             | ordereddict([('glob', '$(inputs.out_file)')]) | Steffen Brinckmann |
| libremsconvert.cwl   | Uses Proteowizard MSConvert to convert an mzXML file into mzML | mzXML file format           | ordereddict([('glob', '*.mzML')])             | Steffen Neumann    |
| osc2hdf.cwl         | convent osc file to hdf5 file                                  | osc file                    | ordereddict([('glob', '$(inputs.out_file)')]) | Steffen Brinckmann |
| png2jpg.cwl         | Convert png to jpg image                                       | png file format             | ordereddict([('glob', '$(inputs.out_file)')]) | Steffen Brinckmann |
| msconvert.cwl | Uses Proteowizard MSConvert to convert vendor files into mzML  | mzXML or vendor file format | ordereddict([('glob', '*.mzML')])             | Steffen Neumann    |