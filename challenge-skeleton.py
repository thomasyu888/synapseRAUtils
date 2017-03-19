'''What it does:
   ...
   
Input:  Synapse employee user name, Synapse employee user password, Challenge Team name, Challenge Project name
Output: The skeleton for two challenges site with initial wiki, two teams (admin and participants), 
        and a challenge wedget added on live site with a participant team associated with it. 

Example (run on bash): python challenge-skeleton.py me mypass multi-driver

Code - Status: in progress
    TODO: 
        1) pass strings with ASCII space
        2) try to create, then catch error if challenge or team exists 
        3) add admin team to both sites with admin access 
        4) add participants

Unit Testing: 
'''
import sys
import os
import json 
import synapseutils
import synapseclient
from synapseclient import Entity, Project, Team

def login(syn, user_name, user_pass):
    syn.login(user_name, user_pass)

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
'''list of user parameters:
   Synapse employee user name: sys.argv[1]
   Synapse employee user pass: sys.argv[2]
   
        Challenge Team name:         sys.argv[3] # without space 
        Challenge Project name:      sys.argv[4] # TODO: pass strings with ASCII space
        
   # TODO: try to create, then catch error if challenge or team exists 
   # TODO: replace with argparser
'''
    user_name = sys.argv[1]
    user_pass = sys.argv[2]
    team_name = sys.argv[3]
    project_name = 'X-Driver prediction Dream challeneg' 

    '''Sage bionetworks employee login
       TODO: change to case where user is known/remembered via api 
    '''
    syn = synapseclient.Synapse()
    login(syn, user_name, user_pass) 

    '''Create two teams for challenge sites.
       1) participant and 2) administrator
    '''
    team_part = team_name  + ' Participants'
    team_admin = team_name  + ' Admin'
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
       ID as source and new challenge project entity syn ID as destination.
    '''
    source_project_id = 'syn2769515' 

    copyChallengeWiki(syn, source_project_id, project_live)
    copyChallengeWiki(syn, source_project_id, project_staging)

    '''Create challenge widget on live challenge site with an associated participant team'''
    createChallengeWidget(syn, project_live, team_part)

if __name__ == "__main__":
    main()



