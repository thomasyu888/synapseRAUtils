import json
import urllib
import pandas
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


raw_dat = urllib.urlopen(standard_path).read()
json_record  = json.loads(raw_dat)
record_flatten = (flatten(d) for d in json_record)
df = pandas.DataFrame(record_flatten)








