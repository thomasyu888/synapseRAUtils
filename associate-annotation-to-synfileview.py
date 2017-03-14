
'''
	What it Does: 
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
from pprint import pprint
import synapseutils
import synapseclient

# annot_path = '/synapseAnnotations/minimal_Sage_standard.yml'
annot_path = '/synapseAnnotations/minimal_Sage_standard.json'

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

'''
	Subset synapse dictionary based on users schema (colnames)
'''
print(annot_dictionary.keys())

user_schema = ['assay', 'dataType', 'dataSubtype', 'fileFormat', 'species']
print(type(user_schema))

subset_annot_dictionary = {k: annot_dictionary[k] for k in user_schema}

# return None if dictionary key is not available
mysubset_annot_dictionary = {k: annot_dictionary.get(k, None) for k in user_schema}
pprint(subset_annot_dictionary)
pprint(mysubset_annot_dictionary)

# subset values of dictionary based on file ID 



# parse through a file View and annotate them based on user-defined schema association (file name | synapse ID , annotation)
# !!! Only works if file view (and its associated files) exist !!! 

''' 
syn = synapseclient.Synapse()
syn.login()

fileViewIds = ["syn ID here"]
fileView = syn.tableQuery("select * from" + fileViewIds)
[f[3] for f in fileView] # list of all files' synID 

''' 

''' 
	for each row in file view 
	syn.get 
	syn.set annotations (is in current optimization process to limit row-wise access for time complexity and efficiency)

'''

'''
Will there be many file views to annotate ? 

for i in fileView:
	r = syn.get(i[1],downloadFile = False)
    print(r)
'''






