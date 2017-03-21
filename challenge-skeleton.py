'''What it does:
   ...
   
Input:  Synapse employee user name, Synapse employee user password, Challenge Team name, Challenge Project name
Output: The skeleton for two challenges site with initial wiki, two teams (admin and participants), 
        and a challenge wedget added on live site with a participant team associated with it. 

Example (run on bash): python challenge-skeleton.py me mypass multi-driver

Code - Status: in progress
    TODO:
        1) try to create, then catch error if challenge or team exists
        2) add admin team to both sites with admin access
        3) add participants
        4) use argparser

Unit Testing:
'''
import sys
import os
import json 
import synapseutils
import synapseclient
from synapseclient import Entity, Project, Team

def creatTeam(syn, team_name, desc, privacy):
    syn.store(Team(name=team_name, description=desc, canPublicJoin=privacy))

def creatProject(syn, project_name):
    project = Project(project_name)
    project = syn.store(project)
    return project

def copyChallengeWiki(syn, source_project_id, project):
    destination_project_id = synapseclient.utils.id_of(project)
    synapseutils.copyWiki(syn, source_project_id, destination_project_id) 

def createChallengeWidget(syn, project_live, team_part):
    project_live_id = synapseclient.utils.id_of(project_live)
    team_part_id = syn.getTeam(team_part)['id']

    challenge_object = {'id': u'1000', 'participantTeamId':team_part_id, 'projectId': project_live_id} 
    challenge = syn.restPOST('/challenge', json.dumps(challenge_object))
    challenge = syn.restGET('/entity/' + project_live_id + '/challenge')

def main():

    team_name = sys.argv[1]
    project_name = 'X-Driver prediction Dream challenge'

    '''Sage Bionetworks employee login
    '''
    syn = synapseclient.Synapse()
    syn.login()

    '''Create two teams for challenge sites.
       1) participant and 2) administrator
    '''
    team_part = team_name + ' Participants'
    team_admin = team_name + ' Admin'
    privacy = True
    desc = ''

    creatTeam(syn, team_part, desc, privacy)
    creatTeam(syn, team_admin, desc, privacy)

    '''Create two project entity for challenge sites.
       1) live (public) and 2) staging (private until launch)
    '''
    live = project_name
    staging = project_name + ' - staging'

    project_live = creatProject(syn, live)
    project_staging = creatProject(syn, staging)

    '''A pre-defined wiki project is used as initial template for challenge sites.
       To copy over the template synapseutils.copyWiki() function is used with template 
       ID as source and new challenge project entity synID as destination.
    '''
    source_project_id = 'syn2769515' 

    copyChallengeWiki(syn, source_project_id, project_live)
    copyChallengeWiki(syn, source_project_id, project_staging)

    '''Create challenge widget on live challenge site with an associated participant team'''
    createChallengeWidget(syn, project_live, team_part)

if __name__ == "__main__":
    main()



