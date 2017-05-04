import json
import pandas
import argparse
import synapseclient


def scope2entityview(syn, scope_id, project_id, annot_path, my_view_name):
    # Get required IDs for Synapse properties
    minimal_view_schema_column_names = [x['name'] for x in syn.restGET("/column/tableview/defaults/file")['list']]
    minimal_view_schema_column_ids = [x['id'] for x in syn.restGET("/column/tableview/defaults/file")['list']]

    df = pandas.read_csv(annot_path)

    if {'ROW_VERSION', 'ROW_ID'}.issubset(df.columns):
        df.drop(['ROW_VERSION', 'ROW_ID'], axis=1, inplace=True)

    df.set_index('id', inplace=True, drop=False)
    df_dict = df.T.to_dict()

    # Update files annotations
    for i in df_dict.keys():
        syn_entity = syn.get(i, downloadFile=False)
        annotDicts = df_dict.get(i)
        syn_entity.annotations = annotDicts
        syn_entity = syn.store(syn_entity)
        print(syn_entity)

    # Find the new columns to add to entity-view
    new_cols = list(df.columns[~df.columns.isin(minimal_view_schema_column_names)].dropna())
    col_types = pandas.DataFrame(df[new_cols].dtypes)
    col_types = col_types.replace(['object', 'int64', 'float64'], ['STRING', 'INTEGER', 'FLOAT'])

    # Add your columns with its associated object types
    added_cols = [syn.store(synapseclient.Column(name=k, columnType=col_types.loc[k, 0])) for k in new_cols]
    added_cols_ids = [c['id'] for c in added_cols]

    # All the columns of your new entity-view
    column_ids = minimal_view_schema_column_ids + added_cols_ids

    # Create an empty entity-view with defined scope as folder
    body = {'columnIds': column_ids,
            'concreteType': 'org.sagebionetworks.repo.model.table.EntityView',
            'entityType': 'org.sagebionetworks.repo.model.table.EntityView',
            'name': my_view_name,
            'parentId': project_id,
            'scopeIds': scope_id,
            'type': 'file'}

    # Create a new entity-view
    entity_view = syn.restPOST(uri='/entity', body=json.dumps(body))
    entity_view = syn.get(entity_view)

    # Store your new matrix/data frame to the entity-view
    my_new_view = syn.store(synapseclient.Table(entity_view['id'], df))


def main():
    # Login to synapse
    syn = synapseclient.login()

    # Define user-input
    # example run: python annot-entityview.py --scopeId syn2222 --projectId syn3333
    #             --annotPath ../../../banksy.csv --entityViewName projectABCEntityView
    parser = argparse.ArgumentParser(
        description='Create a new entity-view and update each files annotation in its scope')

    parser.add_argument('--scopeId', help='An entity-views scope synapse id', required=True, type=str)
    parser.add_argument('--projectId', help='An entity-views project parent synapse id', required=True, type=str)
    parser.add_argument('--annotPath', help='Path to annotations .csv files', required=True, type=str)
    parser.add_argument('--entityViewName', help='Your new entity-view name', required=True, type=str)

    # Assign user-input
    args = parser.parse_args()

    scope_id = [args.scopeId.lstrip('syn')]
    project_id = args.projectId
    annot_path = args.annotPath
    my_view_name = args.entityViewName

    # Check synapse types 
    test_project = syn.get(project_id)
    test_project = str(test_project['entityType'])
    test_project = test_project.split('.')[-1]

    test_scope = syn.get(args.scopeId)
    test_scope = str(test_scope['entityType'])
    test_scope = test_scope.split('.')[-1]

    if test_project in 'Project' and test_scope in 'Folder':
        scope2entityview(syn, scope_id, project_id, annot_path, my_view_name)


if '__main__' == __name__:
    main()
