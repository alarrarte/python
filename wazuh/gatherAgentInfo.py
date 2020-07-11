#!/usr/bin/python3
# This script was developed for fun/training purposes 10-7-2020
# It is to be used inside wazuh agents to be registered

# Import required libraries
import requests
import json
import argparse 
import os
import csv


# Functions

# we define/parse the script arguments
def parse_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("--manager", "-m", help="Specify the wazuh manager API address or FQDN", required=True)
   args = parser.parse_args()
   return args
    

# create directory 
def create_agent_dir(name):
    path = name
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of directory %s failed" % path)




# Get Agent information into a list (id, ip, etc)
# REVIEW : Need to fix except to bring also non key found values
def retrieve_agents(base_url):
    agents = []
    url = '{0}{1}'.format(base_url, "/agents?pretty")
    r = requests.get(url, auth=auth, params=None, verify=verify)
    agentsresponse = r.json()
    agentlist = agentsresponse['data']['items']
    
    for agent in agentlist: 
        agent_dict = {
        'agent_id' : '',
        'agent_ip' : '',
        'agent_osname': '',
        'agent_osarch': '',
        'agent_osversion': '',
        'agent_osplatform': '',
        'agent_status': '',
        'agent_name' : ''
        }
        
        try:
            agent_dict['agent_id'] = agent['id']
            agent_dict['agent_ip'] = agent['ip']
            agent_dict['agent_osname'] = agent['os']['name']
            agent_dict['agent_osarch'] = agent['os']['arch']
            agent_dict['agent_osversion'] = agent['os']['version']
            agent_dict['agent_osplatform'] = agent['os']['platform']
            agent_dict['agent_status'] = agent['status']
            agent_dict['agent_name'] = agent['name']
            agents.append(agent_dict)
        except KeyError:
            print("no key found")
    return agents



# creates dir per agent and writes agent related data
def write_agent_csv(agent_list):
    for agent in agent_list:
        agent_name = agent['agent_name']
        row_list = [[ "Agent ID", "Agent IP Address", "OS Name", "OS Arch", "OS Version", "OS Platform", "Agent status"],
                    [ agent['agent_id'], agent['agent_ip'], agent['agent_osname'], agent['agent_osarch'] , agent['agent_osversion'],agent['agent_osplatform'],agent['agent_status']]]
    
        create_agent_dir(agent_name)

        with open(agent_name+"/agent_info.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)


# script
if __name__ == "__main__":
    # parse script arguments
    args = parse_arguments()
    
    # config details
    manager_ip = args.manager
    base_url = "https://" + manager_ip + ":55000"
    auth = requests.auth.HTTPBasicAuth('foo','bar')
    verify = False
    requests.packages.urllib3.disable_warnings()

    # script
    agents = retrieve_agents(base_url)
    write_agent_csv(agents) 


  

    # DEBUG - print our agent list info
    for agent in retrieve_agents(base_url):
        print("Agent info:")
        print(agent['agent_ip'])
        print(agent['agent_id'])
        print(agent['agent_osname'])
        print(agent['agent_osarch'])
        print(agent['agent_osversion'])
        print(agent['agent_osplatform'])
        print(agent['agent_status'])
        print("")

