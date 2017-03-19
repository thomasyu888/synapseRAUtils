'''Get file View query and based on user-defined schema change the annotation values of each matching field 
   !!! Only works if file view (and its associated schema) exist !!! 
'''
import synapseclient
import synapseutils 
import pandas 
import os 

src_path = 'userDefined_annotations.csv'
fileViewIds = ["syn8455906"] 
fileView = []
query = "select * from "
tag = "id" # is this consistant through synapse 
file_name = 'updated_annotations.csv'

# TODO: check src and dst absolute path 
# TODO: check user input 
# TODO: check columns length and set membership 
# TODO: filter by rows (query = allow where clause)
# TODO: Do we need to change id to synapseID?
# TODO: argparser

def get_csv(path):
	path = os.path.abspath(path)
	df = pandas.read_csv(path, index_col='synapseId')
	return(df)

def fast_access(df):
	df = df.T 
	dc = df.to_dict()
	return df, dc

def connect_synclient():
	syn = synapseclient.Synapse()
	syn.login()
	return(syn)

def query2df(syn, query, index, fileViewIds):
	view = syn.tableQuery(query + fileViewIds[index])
	df = view.asDataFrame()
	return(df)

def uniqueIds(df, tag):
	unique_file_synIds = set(df[tag])
	return(unique_file_synIds)

if '.csv' not in src_path: 
	print("User-defined annotations is not a csv file")
	
else:
	syn = connect_synclient()

	'''use-case: Multiple file-views to annotate'''
	if len(fileViewIds) > 1:
		for i, element in enumerate(fileViewIds):
			index = i	
			view_df = query2df(syn, query, index, fileViewIds)
			file_synIds = uniqueIds(view_df, tag) 
			fileView.append(file_synIds)
			# print(fileView)

	'''use-case: Only one file-view to annotate''' 
	if len(fileViewIds) == 1:
		index = 0	
		view_df = query2df(syn, query, index, fileViewIds)
		file_synIds = uniqueIds(view_df, tag) 
		fileView.append(file_synIds)
		# print(fileView[0])

	user_df = get_csv(src_path)

	'''make files indecies of your dataframe'''
	if tag in view_df.columns: 
		view_df = view_df.set_index(tag)
		view_df.index.name = 'synapseId'

	'''replace annotation based on user annotations where synID's match (pandas matches indexes)'''
	view_df[user_df.columns] = user_df

	'''save as csv file'''
	dst_path = os.path.abspath('.') + file_name
	view_df.to_csv(path_or_buf=dst_path, sep=',')
