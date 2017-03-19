'''What it Does: 
Create a user defined annotation mapping to each files synapse id. 
	1) Read sage annotations dictionary (File type: yml or jason)
	2) Subset dictionary from sage minimal annotations based on an example study
	3) Associate file names (file synapse ID) to their annotations and create a 
	pandas meta-data or dictionary (file name | synapse ID , annotation)

Input: sage annotation path, list of subset keys, 
Output:
'''

import json
import yaml
import csv 
import pandas 
from pprint import pprint

# annot_path = '/.../synapseAnnotations/minimal_Sage_standard.yml'
annot_path = '/.../synapseAnnotations/minimal_Sage_standard.json'

if '.json' in annot_path:
	with open(annot_path, 'r') as j: 
	    annot_dictionary = json.load(j)
	pprint(annot_dictionary)

if '.yml' in annot_path:
	with open(annot_path, 'r') as y:
	    try:
	    	annot_dictionary = yaml.load(y)
	    except yaml.YAMLError as exc:
	        print(exc)
	pprint(annot_dictionary)

print(type(annot_dictionary))

#Subset synapse dictionary based on users schema (colnames)
print(annot_dictionary.keys())

user_schema = ['assay', 'dataType', 'dataSubtype', 'fileFormat', 'species']
print(type(user_schema))

subset_annot_dictionary = {k: annot_dictionary[k] for k in user_schema}

# return None if dictionary key is not available
mysubset_annot_dictionary = {k: annot_dictionary.get(k, None) for k in user_schema}
pprint(subset_annot_dictionary)
pprint(mysubset_annot_dictionary)

# subset values of dictionary based on file ID 
# filename = 'ntap_ncats_annotation_manifest.csv'

# csv_delimiter = ','
# data =[]

# with open(filename, 'rb') as csvfile:
# 	# csvreader = csv.reader(csvfile, delimiter=csv_delimiter)
# 	data = [row for row in csv.reader(csvfile.read().splitlines())]
# 	# for row in csvreader:
# 	# 	data.append(map(float, row))    
# print(data)

# with open('ntap_ncats_annotation_manifest.csv', 'r') as f:
# 	reader = csv.reader(f)

# print(reader)

import pandas as pd
filename = 'userDefined_annotations.csv'
user_metaData_annotation = pd.read_csv(filename, index_col='synapseId')

print(type(user_metaData_annotation))

# user_metaData_annotation.set_index('synapseId').to_dict()
# user_metaData_annotation = user_metaData_annotation.to_dict()
# print(type(user_metaData_annotation))
# print(user_metaData_annotation.keys())

t_data = user_metaData_annotation.transpose() # column access is faster 
t_data = t_data.to_dict()

print(t_data.get('syn8450577'))
print(t_data.keys()) # now all the synIDs are keys

# add these files by synID to a folder then create a fileview from them

'''for i in t_data.keys():
	this = t_data.get(i)
	# synEntity = syn.get(i[1],downloadFile = False)
	print(this)
	#this = t_data.get(i)
	#print(this)'''


# parse through a file View and annotate them based on user-defined schema association (file name | synapse ID , annotation)
# example syn8450784
# !!! Only works if file view (and its associated files) exist !!! 
import synapseclient
import synapseutils 

syn = synapseclient.Synapse()
syn.login()

# fileViewIds = ["syn8450784"] need to join each id to the query 
fileView = syn.tableQuery("select * from syn8450784")


'''if 'syn' in f[2]:
	print "yes"
	[f[2] for f in fileView] # list of all files' synID
else 
	print "this is not the generator list containing the file view ids - fix: switch f[x] in code"
'''

''' 
	for each row 
	syn.get 
	syn.set annotations (in current optimization process to be removed)

'''
# dictionary mapping for funcions (switch statement) to check for different use cases 
# Will there be many file views to annotate? 

for i in t_data.keys():
	synEntity = syn.get(i,downloadFile = False)
	annotDicts = t_data.get(i)
	synEntity.annotations.update(annotDicts)	# will overwrite the current annotations 
	synEntity = syn.store(synEntity)
	print(synEntity)









