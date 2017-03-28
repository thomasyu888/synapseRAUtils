import os
import yaml
import json
import urllib

src = "Data/"
dst = "Results/combined.json"

json_files = [j for j in os.listdir(src) if j.endswith('.json')]
yml_files = [y for y in os.listdir(src) if y.endswith('.yml')]

json_data = {}
yml_data = {}

for file_name in json_files:
	with open(file_name) as current_file:
		j_dat = json.load(current_file)
	json_data.update(j_dat)
	print(len(json_data.keys()))

for file_name in yml_files:
	with open(file_name) as current_file:
		y_dat = yaml.safe_load(current_file)
	yml_data.update(y_dat)
	print(len(yml_data.keys()))

json_data.update(yml_data)
combined_data = json_data

with open(dst, 'w') as outfile:
    json.dump(combined_data, outfile, indent=4, sort_keys=True)


