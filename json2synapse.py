import json
import urllib
import pandas
import numpy
import argparse
import flatten_json
import synapseclient 
from flatten_json import flatten
from pandas.io.json import json_normalize

syn = synapseclient.login()

standard_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_standard.json'
analysis_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/common/minimal_Sage_analysis.json'
dhart_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/dhart_annotations.json'
genie_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/genie_annotations.json'
neuro_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/neuro_annotations.json'
nf_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/nf_annotations.json'
ngs_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/ngs_annotations.json'
onc_path = 'https://raw.githubusercontent.com/Sage-Bionetworks/synapseAnnotations/master/synapseAnnotations/data/onc_annotations.json'

paths = [standard_path, analysis_path, dhart_path, genie_path, neuro_path, nf_path, ngs_path, onc_path]
names = ['standard', 'analysis', 'dhart', 'genie', 'neuro', 'nf', 'ngs', 'onc']
annotations = []

def json2flatten(path, project):	
	# fetch and read raw json objects from its github url and decode the json object to its raw format  
	raw_dat = urllib.urlopen(standard_path).read()
	json_record  = json.loads(raw_dat)
	# Apply flatten (https://github.com/amirziai/flatten) to each element of json record and read it into a pandas dataframe
	record_flatten = (flatten(d) for d in json_record)
	df = pandas.DataFrame(record_flatten)
	# Replace NaN objects with empty strings 
	df = df.replace(numpy.nan, '', regex=True)
	df.loc[:,'category'] = project
	return(df)
json2flatten(nf_path, 'nf')

for project, path in [(n, url) for n in names for url in paths]:
	data = json2flatten(path, project)
	annotations.append(data)
	# print(data)

annotations_df = pandas.concat(annotations)
print(annotations_df, annotations_df.shape)











