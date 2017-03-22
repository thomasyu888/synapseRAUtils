'''practice restful API calls to synapse file view 
Format helps nasim to parse through steps. It will change after comfort zone threshold has been reached.
'''
import synapseclient
import synapseutils 
import pandas
import json 
import requests

syn = synapseclient.Synapse()
syn.login()

#############################################################################################

# new docs http://docs.synapse.org/rest/

#############################################################################################
# make a query bundle request to start an asynchronous job to query a FileView
#############################################################################################

query = {"concreteType":"org.sagebionetworks.repo.model.table.Query", "sql":"select * from syn8459602"}
q = {"concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest", "query": query, "entityId": "syn8459602"}
q = json.dumps(q)
async_id = syn.restPOST(uri='/entity/syn8459602/table/query/async/start', body=q)

# Get the asynchronous job results for a FileView query.
result = syn.restGET(uri='/entity/syn8459602/table/query/async/get/' + str(async_id['token']))
# pd.DataFrame(dict([(k,pd.Series(v)) for k,v in result.iteritems() ]))

#############################################################################################
# table request 
#############################################################################################

csv_req = {"concreteType":"org.sagebionetworks.repo.model.table.CsvTableDescriptor"}
table = {"concreteType":"org.sagebionetworks.repo.model.table.DownloadFromTableRequest", "csvTableDescriptor": csv_req,"sql":"select * from syn8459602", "entityId": "syn8459602"}
table = json.dumps(table)
table_id = syn.restPOST(uri= '/entity/syn8459602/table/download/csv/async/start/', body=table)
view_csv = syn.restGET(uri= '/entity/syn8459602/table/download/csv/async/get/' + str(table_id['token']))

#############################################################################################
# CSV file POST to file view 
#############################################################################################
# TODO:





#############################################################################################
# users csv file upload 
#############################################################################################

filename = 'userDefined_annotations.csv'
user_metaData_annotation = pandas.read_csv(filename, index_col='synapseId')

t_data = user_metaData_annotation.transpose() # column access is faster 
t_data = t_data.to_dict()

#############################################################################################
# practice zone 
# syn.getUserProfile() # syn works?
'''
	command found on file view wiki 
	syn.restGET('/column/fileview/default') raises a 404 file not found error. Possibly default does not exist ?
	 '/column/fileview/default’ was not found on synapse rest api docs or in synapsePythonClient. Only on wiki. 
'''

''' 
	synapse python client uses requests library:
	https://github.com/Sage-Bionetworks/synapsePythonClient/blob/8b57608f6a1b37adbbbca2bf9ba329ca12ee0abd/synapseclient/client.py#L3349 
	http://docs.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests 
'''

syn.restGET('/entity/syn8459602/')
entity = syn.restGET('/entity/{id}/')
entity['annotations']

'''
synapseclient.exceptions.SynapseHTTPError: 400 Client Error: Bad Request
org.sagebionetworks.schema.adapter.JSONObjectAdapterException: org.json.JSONException: JSONObject["query"] is not a JSONObject.; nested exception is org.sagebionetworks.schema.adapter.JSONObjectAdapterException: org.sagebionetworks.schema.adapter.JSONObjectAdapterException: org.json.JSONException: JSONObject["query"] is not a JSONObject.
'''
#############################################################################################

