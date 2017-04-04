import os
import csv
import yaml
import json
import urllib
import pandas 
import synapseclient 
from synapseclient import Entity, Project, Folder, File, Link, Team
import synapseclient.utils as utils

## silent=True optional 
syn = synapseclient.login()
src = "Data/"
json_data = {}

json_files = [j for j in os.listdir(src) if j.endswith('.json')]

for file_name in json_files:
	file_name = "Data/" + file_name
	with open(file_name) as current_file:
		j_dat = json.load(current_file)
	json_data.update(j_dat)

## Mouse ATAC-Seq parent folder syn7315805 parent entity syn7315805 
ATAC_Seq = syn.chunkedQuery('SELECT id,name FROM file WHERE parentId=="syn8415612"')
ATAC_Seq = pandas.DataFrame(list(ATAC_Seq))
ATAC_Seq.columns = ['id', 'name']

#ATAC_Seq_file_names = [f['file.name'] for f in ATAC_Seq]
#ATAC_Seq_file_id = [f['file.id'] for f in ATAC_Seq]

## Mouse RNA-Seq parent folder RNA-seq syn8415608 parent folder syn7315805 parent entity syn7315805
RNA_Seq = syn.chunkedQuery('SELECT id,name FROM file WHERE parentId=="syn8464295"')
RNA_Seq = pandas.DataFrame(list(RNA_Seq))
RNA_Seq.columns = ['id', 'name']
#RNA_Seq_file_names = [f['file.name'] for f in RNA_Seq]
#RNA_Seq_file_id = [f['file.id'] for f in RNA_Seq]

## add keys as columns/series 
schema = list(json_data.keys())
schema = [f.encode("utf-8") for f in schema]
schema.insert(0, "individualID")
 
sara_keys = ['assay',
			 'dataType',
			 'dataSubtype',
			 'fileFormat',
			 'isCellLine',
			 'species',
			 'tissue',
			 'organ',
			 'diagnosis',
			 'tumorType',
			 'cellType',
			 'fundingAgency',
			 'consortium',
			 'specimenID',
			 'individualID',
			 'specimenIdSource',
			 'individualIdSource',
			 'modelSystemName',
			 'analysisType',
			 'rnaAlignmentMethod',
			 'dnaAlignmentMethod',
			 'peakCalllingMethod',
			 'transcriptQuantificationMethod',
			 'runType',
			 'isStranded',
			 'libraryPrep',
			 'readLength',
			 'cellSubType',
			 'platform',
			 'experimentalCondition',
			 'experimentalTimePoint',
			 'timePointUnit',
			 'transplantationType',
			 'transplantDonorSpecies',
			 'transplantDonorTissue',
			 'transplateRecipientTissue']

sara_dict = {k: [] for k in sara_keys}

not_in_schema = []
for i in set(sara_dict.keys()):
	if i not in set(schema):
		not_in_schema.append(i)
		print i

schema.extend(not_in_schema)

RNA_Seq = pandas.concat([RNA_Seq,pandas.DataFrame(columns=schema)], axis=1)
ATAC_Seq = pandas.concat([ATAC_Seq,pandas.DataFrame(columns=schema)], axis=1)

## update annotations 
def csbc_annot(dat):
	dat.ix[dat.name.str.contains('_N'), 'individualID'] = 'N'
	dat.ix[dat.name.str.contains('_E'), 'individualID'] = 'E'
	dat.ix[dat.name.str.contains('_L'), 'individualID'] = 'L'
	dat.ix[dat.name.str.contains('_ML') & ~dat['name'].str.contains('_noLM'), 'individualID'] = 'ML'
	dat.ix[dat.name.str.contains('_ML') & dat['name'].str.contains('_noLM'), 'individualID'] = 'ML_NoLM'
	dat.ix[dat.name.str.contains('_M') & ~dat['name'].str.contains('ML'), 'individualID'] = 'M'

	dat.ix[(dat.individualID == 'N') | (dat.individualID == 'E') | (dat.individualID == 'M'), 'modelSystem'] = 'C57BL/6'
	dat.ix[(dat.individualID == 'L') | (dat.individualID == 'ML') | (dat.individualID == 'ML_NoLM'), 'modelSystem'] = 'ASTxCre-ERT2'
	dat.species = 'mouse'
	dat.cellType = 'CD8+ T Cells'
	dat.ix[~dat.name.str.contains('ML'), 'diagnosis'] = 'Listeriosis'
	dat.ix[dat.name.str.contains('ML'), 'diagnosis'] = 'hepatocellular carcinoma'


	dat.ix[dat.name.str.contains('_N'), 'cellSubType'] = 'naive'
	dat.ix[dat.name.str.contains('_E'), 'cellSubType'] = 'effector'
	dat.ix[dat.name.str.contains('_L'), 'cellSubType'] = 'tumor-infiltrating'
	dat.ix[dat.name.str.contains('_M'), 'cellSubType'] = 'memory'

	dat.transplantationType = 'allograft'
	dat.transplantationDonorTissue = 'TCR TAG transgenic CD8 T cells'
	dat.transplantationRecipientTissue = 'blood'

	dat.ix[dat.name.str.contains('_N'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_E'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_M') & ~dat['name'].str.contains('ML'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_L'), 'experimentalCondition'] = 'hepatocellular carcinoma'

	dat.timePointUnit = 'days'
	return(dat)

RNA_Seq = csbc_annot(RNA_Seq)
ATAC_Seq = csbc_annot(ATAC_Seq)

## write to csv file 
RNA_Seq.to_csv("Results/RNA_Seq.csv", sep=',', index=False)
ATAC_Seq.to_csv("Results/ATAC_Seq.csv", sep=',', index=False)

