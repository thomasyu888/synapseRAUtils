'''What it does:
   ...
   
Input:  Challenge Project name
Output: The skeleton for two challenges site with initial wiki, two teams (admin and participants), 
        and a challenge wedget added on live site with a participant team associated with it. 

Example (run on bash): python challenge-skeleton.py myChallengeName

Code - Status: in progress
    TODO:
        1) try to create, then catch error if challenge or team exists
        3) add participants

Unit Testing:
'''
import json 
import synapseutils
import synapseclient
import argparse
import getpass
from synapseclient import Entity, Project, Team, Wiki

def synapseLogin():
    try:
        syn = synapseclient.login()
    except Exception as e:
        print("Please provide your synapse username/email and password (You will only be prompted once)")
        Username = raw_input("Username: ")
        Password = getpass.getpass()
        syn = synapseclient.login(email=Username, password=Password,rememberMe=True)
    return(syn)

def creatTeam(syn, team_name, desc, privacy):
    team = syn.store(Team(name=team_name, description=desc, canPublicJoin=privacy))
    return(team.id)

def creatProject(syn, project_name, teamId):
    project = Project(project_name)
    project = syn.store(project)
    syn.setPermissions(project, teamId, ['CREATE', 'DOWNLOAD', 'READ', 'UPDATE', 'DELETE', 'CHANGE_PERMISSIONS', 'DOWNLOAD', 'UPLOAD'])
    return(project)

def copyChallengeWiki(syn, source_project_id, project):
    destination_project_id = synapseclient.utils.id_of(project)
    synapseutils.copyWiki(syn, source_project_id, destination_project_id) 

def creatLivePage(syn, project, teamId):
    live_page_markdown = '## Banner\n\n\n**Pre-Registration Open:**\n**Launch:**\n**Close:**\n\n\n\n${jointeam?teamId=%s&isChallenge=true&isMemberMessage=You are Pre-registered&text=Pre-register&successMessage=Successfully joined&isSimpleRequestButton=true}\n> Number of Pre-registered Participants: ${teammembercount?teamId=%s} \n> Click [here](http://s3.amazonaws.com/geoloc.sagebase.org/%s.html) to see where in the world solvers are coming from. \n\n#### OVERVIEW - high level (same as DREAM website?) - for journalists, funders, and participants\n\n\n#### Challenge Organizers / Scientific Advisory Board:\n\n#### Data Contributors:\n\n#### Journal Partners:\n\n#### Funders and Sponsors:' % (teamId, teamId, teamId)
    syn.store(Wiki(title='', owner=project, markdown=live_page_markdown))

def createChallengeWidget(syn, project_live, team_part):
    project_live_id = synapseclient.utils.id_of(project_live)
    team_part_id = syn.getTeam(team_part)['id']

    challenge_object = {'id': u'1000', 'participantTeamId':team_part_id, 'projectId': project_live_id} 
    challenge = syn.restPOST('/challenge', json.dumps(challenge_object))
    challenge = syn.restGET('/entity/' + project_live_id + '/challenge')

def main(challenge_name):

    '''Sage Bionetworks employee login
    '''
    syn = synapseLogin()

    '''Create two teams for challenge sites.
       1) participant and 2) administrator
    '''
    team_part = challenge_name + ' Participants'
    team_admin = challenge_name + ' Admin'
    team_preReg = challenge_name + ' Preregistrants'
    privacy = True
    desc = ''

    team_part_id = creatTeam(syn, team_part, desc, privacy)
    team_admin_id = creatTeam(syn, team_admin, desc, privacy)
    team_preReg_id = creatTeam(syn, team_preReg, desc, privacy)

    '''Create two project entity for challenge sites.
       1) live (public) and 2) staging (private until launch)
    '''
    live = challenge_name
    staging = challenge_name + ' - staging'

    project_live = creatProject(syn, live, team_admin_id)
    project_staging = creatProject(syn, staging, team_admin_id)

    '''A pre-defined wiki project is used as initial template for challenge sites.
       To copy over the template synapseutils.copyWiki() function is used with template 
       ID as source and new challenge project entity synID as destination.
    '''
    source_project_id = 'syn2769515' 

    creatLivePage(syn, project_live, team_preReg_id)
    copyChallengeWiki(syn, source_project_id, project_staging)

    '''Create challenge widget on live challenge site with an associated participant team'''
    createChallengeWidget(syn, project_live, team_part)

def command_main(args):
    main(args.challengeName)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("challengeName", help="Challenge name")
    args = parser.parse_args()
    command_main(args)




