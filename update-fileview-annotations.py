import os
import json
import csv
import pandas
import synapseutils
import synapseclient
from synapseclient import Entity, Project, Folder, File, Link, Team

# user input
src_path = 'userDefined_annotations.csv'
tableId = 'syn8455906'

# Variables 
synID = 'id'
query = 'select * from '
updated_file_name = tableId + '_updated_annotations.csv'

def csv2df(path):
    path = os.path.abspath(path)
    df = pandas.read_csv(path, index_col='id')
    return df

def query2df(syn, query, tableId):
    view = syn.tableQuery(query + tableId)
    view = list(csv.DictReader(file(view.filepath)))
    df = pandas.DataFrame(view)
    return df

syn = synapseclient.login(silent=True)

view_df = query2df(syn, query, tableId)
view_df.set_index(synID, inplace=True, drop=False)
view_df.index.name = 'id' 

user_df = csv2df(src_path)

view_df.update(user_df)

dst_path = os.path.abspath('.') + '/' + updated_file_name
view_df.to_csv(path_or_buf=dst_path, sep=',', index=False)

# information on rest api calls as transaction 
# http://docs.synapse.org/rest/index.html
# http://docs.synapse.org/rest/org/sagebionetworks/repo/model/table/TableUpdateRequest.html

# Credit: https://gist.github.com/kdaily/0db938589a08f0c7d8317d0cf2924167#file-tableUpdateTransaction-py
file_handle_id = synapseclient.multipart_upload.multipart_upload(syn, updated_file_name)

uploadRequest = {u'tableId': tableId, u'linesToSkip': 0, u'concreteType': u'org.sagebionetworks.repo.model.table.UploadToTableRequest', u'uploadFileHandleId': file_handle_id, 
                 u'csvTableDescriptor': {u'escapeCharacter': u'\\', u'isFirstLineHeader': True, u'separator': u',', u'lineEnd': '\n', u'quoteCharacter': u'"'}}

request = {u'concreteType': u'org.sagebionetworks.repo.model.table.TableUpdateTransactionRequest',
           u'entityId': tableId,
           u'changes': [uploadRequest]}

endpoint = 'https://repo-prod.prod.sagebase.org/repo/v1'
uri = '/entity/{tableId}/table/transaction/async/'.format(tableId=tableId)
result = syn._waitForAsync(uri, request, endpoint)






