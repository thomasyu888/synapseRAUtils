import os
import csv
import yaml
import json
import urllib
import pandas 
import numpy 
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
		#print i

schema.extend(not_in_schema)

RNA_Seq = pandas.concat([RNA_Seq, pandas.DataFrame(columns=schema)], axis=1)
ATAC_Seq = pandas.concat([ATAC_Seq, pandas.DataFrame(columns=schema)], axis=1)


## update annotations 
def csbc_annot(dat):
	## individualID
	dat.ix[dat.name.str.contains('_N'), 'individualID'] = 'N'
	dat.ix[dat.name.str.contains('_E'), 'individualID'] = 'E'
	dat.ix[dat.name.str.contains('_L'), 'individualID'] = 'L'
	dat.ix[dat.name.str.contains('_ML') & ~dat.name.str.contains('_noLM'), 'individualID'] = 'ML'
	dat.ix[dat.name.str.contains('_ML') & dat.name.str.contains('_noLM'), 'individualID'] = 'ML_NoLM'
	dat.ix[dat.name.str.contains('_M') & ~dat.name.str.contains('ML'), 'individualID'] = 'M'

	## modelSystem
	dat.ix[(dat.individualID == 'N') | (dat.individualID == 'E') | (dat.individualID == 'M'), 'modelSystem'] = 'C57BL/6'
	dat.ix[(dat.individualID == 'L') | (dat.individualID == 'ML') | (dat.individualID == 'ML_NoLM'), 'modelSystem'] = 'ASTxCre-ERT2'
	
	## species (which string on sample indicates this information ?)
	dat.species = 'mouse'

	## transplantationDonorSpecies
	dat.transplantationDonorSpecies = 'mouse'

	## cellType (which string on sample indicates this information ?)
	dat.cellType = 'CD8+ T Cells'

	## diagnosis 
	dat.ix[~dat.name.str.contains('ML'), 'diagnosis'] = 'Listeriosis'
	dat.ix[dat.name.str.contains('ML'), 'diagnosis'] = 'hepatocellular carcinoma'

	## cellSubType
	dat.ix[dat.name.str.contains('_N'), 'cellSubType'] = 'naive'
	dat.ix[dat.name.str.contains('_E'), 'cellSubType'] = 'effector'
	dat.ix[dat.name.str.contains('_L'), 'cellSubType'] = 'tumor-infiltrating'
	dat.ix[dat.name.str.contains('_M'), 'cellSubType'] = 'memory'

	## transplantationType
	dat.transplantationType = 'allograft'

	## transplantationDonorTissue
	dat.transplantationDonorTissue = 'TCR TAG transgenic CD8 T cells'

	## transplantationRecipientTissue
	dat.transplantationRecipientTissue = 'blood'

	## experimentalCondition
	dat.ix[dat.name.str.contains('_N'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_E'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_M') & ~dat['name'].str.contains('ML'), 'experimentalCondition'] = 'ListeriaTAG immunization'
	dat.ix[dat.name.str.contains('_L'), 'experimentalCondition'] = 'hepatocellular carcinoma'

	## timePointUnit
	dat.timePointUnit = 'days'

	## assay 
	dat.ix[dat.name.str.contains('RNA'), 'assay'] = 'rnaSeq'
	dat.ix[dat.name.str.contains('ATAC'), 'assay'] = 'ATACSeq'

	## dataType
	dat.ix[dat.name.str.contains('RNA'), 'dataType'] = 'geneExpression'
	dat.ix[dat.name.str.contains('ATAC'), 'dataType'] = 'chromatinAcitivity'

	## dataSubtype
	dat.ix[dat.name.str.contains('.txt.gz'), 'dataSubtype'] = 'processed'
	dat.ix[dat.name.str.contains('.fastq.gz'), 'dataSubtype'] = 'raw'

	## fileFormat
	dat.ix[dat.name.str.contains('.txt.gz'), 'fileFormat'] = 'txt'
	dat.ix[dat.name.str.contains('.fastq.gz'), 'fileFormat'] = 'fastq'

	## isCellLine 
	dat.isCellLine = False

	## tissue
	dat.tissue = 'spleenocytes'

	## organ 
	dat.organ = 'spleen'

	## tumorType	
	dat.tumorType = 'Not Applicable'

	## fundingAgency
	dat.fundingAgency = 'NCI'

	## consortium
	dat.consortium = 'CSBC'

	## specimenID
	dat.ix[dat.name.str.contains('_N'), 'specimenID'] = (dat.name.str.split('_').str[2:3]).where(dat.name.str.contains('_N'))
	dat.ix[dat.name.str.contains('_E'), 'specimenID'] = (dat.name.str.split('_').str[2:4]).where(dat.name.str.contains('_E'))
	dat.ix[dat.name.str.contains('_L'), 'specimenID'] = (dat.name.str.split('_').str[2:4]).where(dat.name.str.contains('_L'))
	dat.ix[dat.name.str.contains('_ML') & ~dat.name.str.contains('_noLM'), 'specimenID'] = (dat.name.str.split('_').str[2:4]).where(dat.name.str.contains('_ML') & ~dat.name.str.contains('_noLM'))
	dat.ix[dat.name.str.contains('_ML') & dat.name.str.contains('_noLM'), 'specimenID'] = (dat.name.str.split('_').str[2:5]).where(dat.name.str.contains('_ML') & dat.name.str.contains('_noLM'))
	dat.ix[dat.name.str.contains('_M') & ~dat.name.str.contains('ML'), 'specimenID'] = (dat.name.str.split('_').str[2:3]).where(dat.name.str.contains('_M') & ~dat.name.str.contains('ML'))
	dat.specimenID = dat.specimenID.apply(lambda x: '_'.join(x))

	## specimenIdSource
	dat.specimenIdSource = 'MSKCC'

	## individualIdSource
	dat.individualIdSource = 'individualIdSource'

	## look into GEOquery library 
	dat.modelSystemName = ''

	dat.ix[dat.name.str.contains('RNA'), 'analysisType'] = 'transcriptQuantification'
	dat.ix[dat.name.str.contains('ATAC'), 'analysisType'] = 'peakCalling'

	dat.ix[dat.name.str.contains('RNA') & dat.name.str.contains('.txt'), 'rnaAlignmentMethod'] = 'STAR'
	dat.ix[dat.name.str.contains('ATAC') & dat.name.str.contains('.txt'), 'dnaAlignmentMethod'] = 'bowtie2'

	dat.ix[dat.name.str.contains('ATAC') & dat.name.str.contains('.txt'), 'peakCalllingMethod'] = 'MACS2'
	dat.ix[dat.name.str.contains('RNA') & dat.name.str.contains('.txt'), 'transcriptQuantificationMethod'] = 'DeSeq2'

	dat.runType  = 'pairedEnd'
	dat.isStranded = True

	dat.ix[dat.name.str.contains('RNA'), 'libraryPrep'] = 'polyASelection'
	dat.readLength = '50'
	dat.platform = 'HiSeq2500'

	## experimentalTimePoint

	dat.ix[dat.name.str.contains('_N'), 'experimentalTimePoint'] = (dat.name.str.split('_').str[2:3]).where(dat.name.str.contains('_N')).str[0].str[1]
	dat.ix[dat.name.str.contains('_E'), 'experimentalTimePoint'] = (dat.name.str.split('_').str[2:3]).where(dat.name.str.contains('_E')).str[0].str[1]
	dat.ix[dat.name.str.contains('_L'), 'experimentalTimePoint'] = (dat.name.str.split('_').str[2:3]).where(dat.name.str.contains('_L')).str[0].str[1]
	dat.ix[dat.name.str.contains('_ML') & ~dat.name.str.contains('_noLM'), 'experimentalTimePoint'] = (dat.name.str.split('_').str[2:4]).where(dat.name.str.contains('_ML') & ~dat.name.str.contains('_noLM')).str[0].str[2]
	dat.ix[dat.name.str.contains('_ML') & dat.name.str.contains('_noLM'), 'experimentalTimePoint'] = (dat.name.str.split('_').str[2:4]).where(dat.name.str.contains('_ML') & dat.name.str.contains('_noLM')).str[0].str[2]
	dat.ix[dat.name.str.contains('_M') & ~dat.name.str.contains('ML'), 'experimentalTimePoint'] = '60'

	return dat


RNA_Seq = csbc_annot(RNA_Seq)
ATAC_Seq = csbc_annot(ATAC_Seq)

## write to csv file 
RNA_Seq.to_csv("Results/RNA_Seq.csv", sep=',', index=False)
ATAC_Seq.to_csv("Results/ATAC_Seq.csv", sep=',', index=False)


