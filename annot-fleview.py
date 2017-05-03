import csv
import pandas
import json
import synapseclient

# login to synapse 
syn = synapseclient.login()

## user defined variables 
# list your entity-view scopes and strip the syn string from the synapse ids
my_scope = ['syn8611215'.lstrip('syn')]

# define your parent project 
project_id = 'syn7349745'

# path to new annotations 
annot_path = "minified_tool_manifest_template-46166.csv"

# name of your new entity-view 
my_view_name = 'nasim_test_2'


# Required IDs for Synapse properties
minimal_view_schema_column_names = [x['name'] for x in syn.restGET("/column/tableview/defaults/file")['list']]
minimal_view_schema_column_ids = [x['id'] for x in syn.restGET("/column/tableview/defaults/file")['list']]

df = pandas.read_csv(annot_path)
df.set_index('id', inplace=True, drop=False)
df_dict = df.T.to_dict()

# update files annotations 
for i in df_dict.keys():
	syn_entity = syn.get(i,downloadFile = False)
	annotDicts = df_dict.get(i)
	syn_entity.annotations = annotDicts
	syn_entity = syn.store(syn_entity)
	print(syn_entity)

# find the new columns to add to entity-view  
new_cols = list(df.columns[~df.columns.isin(minimal_view_schema_column_names)].dropna())
col_types = pandas.DataFrame(df[new_cols].dtypes)
col_types = col_types.replace(['object', 'int64', 'float64'], ['STRING', 'INTEGER', 'FLOAT']) 

# add your columns with its associated object types
my_added_cols = [syn.store(synapseclient.Column(name=k, columnType=col_types.loc[k, 0])) for k in new_cols]
my_added_cols_ids = [c['id'] for c in my_added_cols]

# All the columns of your new entity-view 
column_ids = minimal_view_schema_column_ids + my_added_cols_ids

# Create an empty entity-view with defined scope as folder
body = {'columnIds': column_ids,
        'concreteType': 'org.sagebionetworks.repo.model.table.EntityView',
        'entityType': 'org.sagebionetworks.repo.model.table.EntityView',
        'name': my_view_name,
        'parentId': project_id,
        'scopeIds': my_scope,
        'type': 'file'}

# create a new entity-view 
entity_view = syn.restPOST(uri='/entity', body=json.dumps(body))
entity_view = syn.get(entity_view)

# store your new matrix/data frame to the entity-view 
my_new_view  = syn.store(synapseclient.Table(entity_view['id'], df))
