#!/usr/bin/python
# This script was developed for fun/training purposes 10-7-2020
# It is to be used inside wazuh agents to be registered

# Import required libraries
import requests
import json
import argparse 
import os

# Functions

# we define/parse the script arguments
def parse_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("--manager", "-m", help="Specify wazuh manager ip address where the agent will register", required=True)
   parser.add_argument("--agentname","-n", help="Specify the agent hostname", required=True)
   parser.add_argument("--agentip","-i", help="Specify the agent ip address", required=True)
   parser.add_argument("--user", "-u", help="Specify the API user", required=True)
   parser.add_argument("--password", "-p", help="Specify the API password", required=True)
   args = parser.parse_args()
   return args
    
# Agent registration handling
def register_agent(base_url, data):
    url = '{0}{1}'.format(base_url, "/agents?pretty")
    r = requests.post(url, auth=auth, data=data, verify=verify)
    agent = r.json()
    #print(json.dumps(r.json(), indent=4, sort_keys=True))
    #print("Status: {0}".format(r.status_code))
    key = agent['data']['key']
    return key


# import key into the host
def import_key(key):
    cmd = 'yes | /var/ossec/bin/manage_agents -i ' + key
    os.system(cmd)

# restart wazuh-agent service
def restart_agent():
    cmd = 'systemctl restart wazuh-agent'
    os.system(cmd)


# script
if __name__ == "__main__":
    # parse script arguments
    args = parse_arguments()
    
    # config details
    manager_ip = args.manager
    agent_ip = args.agentip
    agent_name = args.agentname
    api_user = args.user
    api_password = args.password
    base_url = "https://" + manager_ip + ":55000"
    auth = requests.auth.HTTPBasicAuth(api_user,api_password)
    verify = False
    data = {"name": agent_name,"ip": agent_ip}
    requests.packages.urllib3.disable_warnings()
    
    # we register the agent and get the key 
    print ('Adding the agent into the manager....')
    key = register_agent(base_url,data)

    # we import the key on the host
    print ('Importing the agent key...')
    import_key(key)

    # we restart the agent 
    print ('restarting wazuh....')
    restart_agent()

    print ('done, check /var/ossec/logs/ossec.log')
