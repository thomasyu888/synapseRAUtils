# parse through a file View and annotate them based on user-defined schema association (file name | synapse ID , annotation)
# example syn8450784
# !!! Only works if file view (and its associated schema) exist !!! 

import synapseclient
import synapseutils 
import pandas as pd
import request 

filename = 'userDefined_annotations.csv'
user_metaData_annotation = pd.read_csv(filename, index_col='synapseId')
t_data = user_metaData_annotation.transpose() # column access is faster 
t_data = t_data.to_dict()

# print(t_data.get('syn8450577'))
# print(t_data.keys()) # now all the synIDs are keys

# connect to synapse

syn = synapseclient.Synapse()
syn.login()

# list of existing file views and associated schema to be annotated 
fileViewIds = ["syn8455906"] 
fileView = []

# use-case: Multiple file views to annotate

if len(fileViewIds) > 1:
	for i, element in enumerate(fileViewIds):	
		view = syn.tableQuery("select * from " + fileViewIds[i])
		file_synIds = [f[2] for f in view]
		file_synIds = set(file_synIds)  
		fileView.append(file_synIds)
		print(fileView)

#  use-case: Only one file view to annotate 

if len(fileViewIds) == 1:
	view = syn.tableQuery("select * from " + fileViewIds[0])
	view_df = view.asDataframe()
	file_synIds = [f[2] for f in view]
	file_synIds = set(file_synIds)
	fileView.append(file_synIds)
	print(fileView[0])

# subset annotation dictionary based on available annotations 

files_to_annot = set(t_data.keys()) & fileView[0]
print("Number of files with annotations: " + str(len(files_to_annot)))
print(files_to_annot)

files_missing_annot = set(t_data.keys()) - fileView[0]
print("Number of files missing annotations: \n" + str(len(files_missing_annot)))

# which don't have annotation (place null/none annotations for them in file view)
# files_missing_annot = [fileView[0] for fileView[0] in files_to_annot if files_to_annot.isdisjoint(fileView[0])]
# print("files missing annotations: \n", files_missing_annot)

''' 
	for each row/ syn file ID
	syn.get() File entity 
	update File entity annotation 

'''
for i in files_to_annot:
	synEntity = syn.get(i, downloadFile = False)
	annotDicts = t_data.get(i)
	synEntity.annotations.update(annotDicts)	# will overwrite the current annotations 
	synEntity = syn.store(synEntity)
	#print(synEntity) 							# test 







