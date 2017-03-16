# Get a generator file view make changes to data frame push up changes to file view 
# !!! Only works if file view (and its associated schema) exist !!! 

import synapseclient
import synapseutils 
import pandas 

path = 'userDefined_annotations.csv'

# list of existing file views and associated existing schema to be annotated 
fileViewIds = ["syn8455906"] 
fileView = []
query = "select * from "
tag = "id"

def getCSV(path):
	# use'synapseId'as col index for now 
	# TODO: pass args to panda read csv
	df = pandas.read_csv(path, index_col='synapseId')
	return(df)

def fastAccess(df):
	# column or key access is faster 
	df = df.transpose() 
	dc = df.to_dict()
	return df, dc

def connectToSynClient():
	syn = synapseclient.Synapse()
	syn.login()
	return(syn)

def downloadQueryAndmakeDf(syn, query, index, fileViewIds):
	view = syn.tableQuery(query + fileViewIds[index])
	df = view.asDataFrame()
	return(df)

def uniqueIds(df, tag):
	unique_file_synIds = set(df[tag])
	return(unique_file_synIds)


syn = connectToSynClient()
# use-case: Multiple file views to annotate

if len(fileViewIds) > 1:
	for i, element in enumerate(fileViewIds):
		index = i	
		view_df = downloadQueryAndmakeDf(syn, query, index, fileViewIds)
		file_synIds = uniqueIds(view_df, tag) 
		fileView.append(file_synIds)
		print(fileView)

#  use-case: Only one file view to annotate 

if len(fileViewIds) == 1:
	index = 0	
	view_df = downloadQueryAndmakeDf(syn, query, index, fileViewIds)
	file_synIds = uniqueIds(view_df, tag) 
	fileView.append(file_synIds)
	print(fileView[0])

print(view_df)