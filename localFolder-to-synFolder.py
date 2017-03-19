'''What it does: 
	Takes a list of files on local machine/server directory (source),  
	subsets the files by pattern-matching (ex. files with '.csv' extension)
	stores them on a synapse data-folder as a synapse File object 
	
Input:
Output: 

Example (bash commandline run): 

Code - Status: in progress
	TODO: argparser
	TODO: abs path check
Unit Testing: 
'''

import sys
import os
import json 
import synapseutils
import synapseclient
from synapseclient import Entity, Project, Folder, File, Link, Team 


# user_name = sys.argv[1] 
# user_pass = sys.argv[2] 
# data_folder_id = sys.argv[3]		# synapse data-folder that is the parent/container of all files 
# file_description = sys.argv[4]
# source_path = sys.argv[5]
# pattern_match = sys.argv[6]

syn = synapseclient.Synapse()
syn.login(user_name, user_pass)

data_folder = syn.get(data_folder_id)

src = source_path
src_files = os.listdir(src)
subset_files = [name for name in src_files if pattern_match in name]

for file_name in subset_files:
    full_file_name = os.path.join(src, file_name)				# append name to file path 
    if (os.path.isfile(full_file_name)):
    	file_entity = File(full_file_name, description=file_description, parent=data_folder)
    	file_entity = syn.store(file_entity)
