#!/usr/bin/python3
import os

for pyFileName in os.listdir('PythonConverter'):
  print('\nUse',pyFileName)
  pyFile = open('PythonConverter/'+pyFileName,'r')
  cwlFile = open(pyFileName[:-2]+'cwl','w')

  cwlFile.write('#!/usr/bin/env cwl-runner'+'\n'*2)
  cwlFile.write('cwlVersion: v1.0'+'\n')
  cwlFile.write('class: CommandLineTool'+'\n')

  #HEADER
  _ = pyFile.readline()
  if pyFile.readline().strip() != '"""':
    print("Error reading head of python file 1")
    break
  label = pyFile.readline()
  cwlFile.write('label: '+label+'\n')
  cwlFile.write('baseCommand: ["sh","script.sh"]'+'\n'*2)
  cwlFile.write('hints:'+'\n')
  cwlFile.write('  DockerRequirement:'+'\n')
  cwlFile.write('    dockerPull: python'+'\n'*2)
  cwlFile.write('inputs:'+'\n')
  cwlFile.write('  in_file:'+'\n')
  cwlFile.write('    type: File'+'\n')
  _ = pyFile.readline()
  if pyFile.readline().strip() != 'in_file:':
    print("Error reading head of python file 2")
    break
  label = pyFile.readline()
  cwlFile.write('  '+label)
  cwlFile.write('    doc: |-'+'\n')
  vendor = pyFile.readline()
  cwlFile.write('    '+vendor)
  software = pyFile.readline()
  cwlFile.write('    '+software)
  cwlFile.write('  out_file:'+'\n')
  cwlFile.write('    type: string'+'\n'*2)
  cwlFile.write('requirements:'+'\n')
  cwlFile.write('  InitialWorkDirRequirement:'+'\n')
  cwlFile.write('    listing:'+'\n')
  cwlFile.write('      # main shell script that starts pip and python'+'\n')
  cwlFile.write('      - entryname: script.sh'+'\n')
  cwlFile.write('        entry: |-'+'\n')
  cwlFile.write('          pip3 install -r requirements.txt'+'\n')
  cwlFile.write('          python convert.py'+'\n')
  cwlFile.write('      # pip install packages'+'\n')
  cwlFile.write('      - entryname: requirements.txt'+'\n')
  cwlFile.write('        entry: |-'+'\n')
  if pyFile.readline().strip() != 'out_file:':
    print("Error reading head of python file 3")
    break
  labelOut = pyFile.readline()  #read now, use later
  # get requirements
  requirements = []
  for line in pyFile:
    if '#CWL requirement' in line:
      requirements.append(line.split()[1].split('.')[0])
  cwlFile.write('          '+' '.join(requirements)+'\n')
  cwlFile.write('      # python script that does the work'+'\n')
  cwlFile.write('      - entryname: convert.py'+'\n')
  cwlFile.write('        entry: |-'+'\n')

  #MAIN PART: parse file
  pyFile.seek(0)
  for i in range(11):
    pyFile.readline()
  while True:
    line = pyFile.readline()
    if line.startswith('fileNameIn ='):
      line = "fileNameIn = '$(inputs.in_file.path)'\n"
    if line.startswith('fileNameOut='):
      line = "fileNameOut= '$(inputs.out_file)'\n"
    line = line.replace('\\x00','\\\\x00')
    if len(line)==0:
      break
    if len(line)>1:
      cwlFile.write('          '+line)
    else:
      cwlFile.write('\n')    #keep empty lines empty

  #FOOTER
  cwlFile.write('\n'*2)
  cwlFile.write('outputs:'+'\n')
  cwlFile.write('  outfile:'+'\n')
  cwlFile.write('    type: File'+'\n')
  cwlFile.write('  '+labelOut)
  cwlFile.write('    format: edam:format_3590'+'\n')
  cwlFile.write('    outputBinding:'+'\n')
  cwlFile.write('      glob: $(inputs.out_file)'+'\n'*2)
  cwlFile.write('s:author:'+'\n')
  cwlFile.write('  - class: s:Person'+'\n')
  cwlFile.write('    s:identifier: https://orcid.org/0000-0003-0930-082X'+'\n')
  cwlFile.write('    s:name: Steffen Brinckmann'+'\n'*2)
  cwlFile.write('$namespaces:'+'\n')
  cwlFile.write('  s: https://schema.org/'+'\n')
  cwlFile.write('  edam: http://edamontology.org/'+'\n')
  cwlFile.write('$schemas:'+'\n')
  cwlFile.write('  - https://schema.org/version/latest/schemaorg-current-http.rdf'+'\n')
  cwlFile.write('  - http://edamontology.org/EDAM_1.18.owl'+'\n')

  pyFile.close()
  cwlFile.close()