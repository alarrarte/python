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



if __name__ == "__main__":
    # parse script arguments
    args = parse_arguments()

    # config details
    # script
    filepath = args.file
    hostnames = process_hostnames(filepath)
    for host in validate_hostnames(hostnames):
        print (host)
