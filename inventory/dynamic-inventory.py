#!/usr/bin/env python
# An Ansible dynamic inventory script must support two command-line flags:

# --host=<hostname> for showing host details

# --list for listing groups

import subprocess
import paramiko
import argparse
import time
import sys
import json 

def args_parse():
    parser = argparse.ArgumentParser(description='Dynamic Inventory for hosts')
    parser.add_argument("--host", help = "Show Output") 
    parser.add_argument("--list", action='store_const', const=1, help = "Listing Groups")
    args = parser.parse_args()
    return args

def get_host_details(hostname):
    cmd = "vagrant ssh-config {}".format(hostname)
    output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    time.sleep(2)
    str_host_info = (list(output.communicate()))[0].decode('utf-8')
    # instantiate SSHConfig parser
    config = paramiko.SSHConfig()
    hostname_details = config.from_text(str_host_info).lookup(hostname)
    return hostname_details

def running_hosts():
    hosts = list()
    cmd = "vagrant status --machine-readable"
    hosts_info_list = subprocess.check_output(cmd.split()).decode('utf-8').split('\n')
    for host_info in hosts_info_list:
        try:
            host_attributes = host_info.split(',')
            hostname_proper = host_attributes[1]
            hostname_state_type = host_attributes[2]
            hostname_current_state = host_attributes[3]
            if hostname_current_state == 'running' and hostname_state_type == 'state':
                hosts.append(hostname_proper)
        except IndexError:
            pass
    return hosts

def main():
    args = args_parse()
    if args.list:
        all_hosts = running_hosts()
        json.dump({"vagrant": all_hosts}, sys.stdout)
    elif args.host:
        specific = get_host_details("vagrant1")
        json.dump(specific, sys.stdout)

if __name__ == '__main__':
    main()

