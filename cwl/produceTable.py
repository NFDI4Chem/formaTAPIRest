import sys, os
import pandas as pd
from ruamel import yaml

dfAll = pd.DataFrame()
dfPart= pd.DataFrame()
for fileName in os.listdir('.'):
  if not fileName.endswith('.cwl'):
  	continue
  print("Start with file:",fileName)
  #start of processing
  with open(fileName, "r") as cwl_h:
	  yaml_obj = yaml.main.round_trip_load(cwl_h, preserve_quotes=True)
  dfAll = dfAll.append(yaml_obj, ignore_index=True)
  if 'in_file' in yaml_obj['inputs']:
      inname = 'in_file'
  elif 'in_dir' in yaml_obj['inputs']:
      inname = 'in_dir'
  if 'outfile' in yaml_obj['outputs']:
      outname = 'outfile'
  elif 'out_dir' in yaml_obj['outputs']:
      outname = 'out_dir'
  if 'outputBinding' in yaml_obj['outputs'][outname]:
      outlink = 'outputBinding'
  elif 'outputSource' in yaml_obj['outputs'][outname]:
      outlink = 'outputSource'

  dset  = {'file name':fileName,
           'label':yaml_obj['label'],
           'input':yaml_obj['inputs'][inname]['label'],
           'input':yaml_obj['inputs'][inname]['format'],
#           'output':yaml_obj['outputs'][outname][outlink],
           'output':yaml_obj['outputs'][outname]['label'],
           'output':yaml_obj['outputs'][outname]['format'],
           'author':yaml_obj['s:author'][0]['s:name']}
  dfPart= dfPart.append(dset, ignore_index=True)

# output
print('\nAll meta data found:')
print(dfAll.columns)

dfPart = dfPart[dset.keys()] #reorder columns as intended
dfPart.to_csv('overview.csv', index=False)
with open('README_stub.md') as fIn:
  readme = fIn.readlines()
with open('README.md','w') as fOut:
  fOut.writelines(readme)
  dfPart.to_markdown(fOut, index=False)
