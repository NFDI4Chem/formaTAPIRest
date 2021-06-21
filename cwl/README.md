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

# Helpful hints
- Labels can be only single line strings without :
- python code can be embedded
  https://rabix.io/cwl.html