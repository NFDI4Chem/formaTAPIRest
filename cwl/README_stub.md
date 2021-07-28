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
