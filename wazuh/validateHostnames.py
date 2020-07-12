#!/usr/bin/python
# This script was developed for fun/training purposes 10-7-2020

# Imports
import argparse
import sys

# Functions

# we define/parse the script arguments
def parse_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("--file", "-f", help="path to client.keys file", required=True)
   parser.add_argument("--continent", "-c", help="Specify the continent to group by", choices=["AS", "AF", "NA", "SA", "AN", "EU", "AU"])
   args = parser.parse_args()
   return args
      
# opens hostnames file
def process_hostnames(filepath):
    hostnames = []
    
    try:
        file = open(filepath, "r")
        for line in file:
            host = line.split(" ",2)[1]
            hostnames.append(host)
        return hostnames

    except FileNotFoundError:
        print("File "+filepath+" not found. Please specify the correct path.")
        sys.exit(1)


# main

# Validates continent is matched
def validate_continent(hostname):
    continent = hostname[0:2]
    
    if continent in [ "AS", "AF", "NA", "SA", "AN", "EU", "AU"]:
        return True
    else:
        return False

# Validates server group is matched
def validate_group(hostname):
    group = hostname[2:5]

    if group in [ "SQL", "WEB", "DAT"]:
        return True
    else:
        return False

# Validates OS is matched
def validate_os(hostname):
    os = hostname[5:8]

    if os in [ "LIN", "WIN"]:
        return True
    else:
        return False

# Validates server number between 000-999
def validate_number(hostname):
    accepted_numbers = []

    for number in range(1000):
        accepted_numbers.append('{0:03}'.format(number))
    
    number = hostname[8:]

    if number in accepted_numbers:
        return True
    else:
        return False

# Validates hostname
def validate_hostnames(hostnames):
    validated_list = []
    for hostname in hostnames:
        if validate_continent(hostname):
            if validate_group(hostname):
                if validate_os(hostname):
                    if validate_number(hostname):
                        validated_list.append(hostname+ " - OK.")
                    else:
                        validated_list.append(hostname+ " - NOT OK.")
                else:
                    validated_list.append(hostname+ " - NOT OK.")
            else:
                validated_list.append(hostname+ " - NOT OK.")
        else:
            validated_list.append(hostname+ " - NOT OK.")
    return validated_list


# Group By continent (list already validated)
# Will not get incorrect named agents
def group_by_continent_server(hostnames,c):
    group = 0
    web = 0
    sql = 0
    dat = 0

    for hostname in hostnames:
        if "- OK." in hostname: 
            continent = hostname[0:2]
            server     = hostname[2:5]
            if (c == continent):
                group += 1
                if server == "WEB":
                    web += 1
                elif server == "SQL":
                    sql += 1
                else:
                    dat += 1
    print("- "+ c +" agents: - Total: "+ str(group) + " - Web: " + str(web) + " - SQL: " + str(sql) + " - DAT: " + str(dat))





if __name__ == "__main__":
    # parse script arguments
    args = parse_arguments()

    # config details
    # script
    filepath = args.file
    hostnames = process_hostnames(filepath)
    validated_hostnames = validate_hostnames(hostnames)
   
    
    if args.continent is not None:
        c = args.continent
        group_by_continent_server(validated_hostnames,c)
    else:
        for hostname in validated_hostnames:
            print (hostname)
