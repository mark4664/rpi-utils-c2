#!/usr/bin/python3

# Script name: chupip.py
# check and update ip address display
# Peter Normington
# 2019-04-07

import datetime
import subprocess
import os
import json

from time import *
from ftplib import FTP

readingDateTime = datetime.datetime.now()
readingDate = str(readingDateTime.strftime("%Y-%m-%d"))
readingTime = str(readingDateTime.strftime("%H:%M:%S"))

# Array variables for the IP addresses, wired and wireless
current_ip = ["",""]
# Array variables for any existing (legacy?) IP addresses: wired, wireless and router
old_ip = ["","",""]

# Get the home directory (eg "/home/dave")
userresult = subprocess.run(['/usr/bin/whoami'], stdout=subprocess.PIPE)
homedir = "/home/"+userresult.stdout.decode('UTF-8').strip()

# Get the hostname (eg "davespi")
hostresult = subprocess.run(['/bin/hostname'], stdout=subprocess.PIPE)
hostname = hostresult.stdout.decode('UTF-8').strip()

# Run ifconfig, which gets more info than we need
ifcfgresult = subprocess.run(['/sbin/ifconfig'], stdout=subprocess.PIPE)
ifcfg = ifcfgresult.stdout.decode('UTF-8')

# Work through the output of ifconfig, extracting the relevant bits
outstr=""
ip_idx = 0
nextline = 0
iflines = ifcfg.strip().split("\n")
for line in ifcfg.splitlines():
    line = line.strip()
    if line.startswith('eth0'):
        outstr+= ("eth0: ")
        nextline = 1
    elif line.startswith('wlan0'):
        outstr+= ("wlan0: ")
        nextline = 1
    elif nextline == 1:
        if line.startswith("inet"):
            current_ip[ip_idx] = line.split()[1]
            outstr+= current_ip[ip_idx]+"\n"
            ip_idx+=1
        else: 
            outstr+="none\n"
            current_ip[ip_idx] = "none"
            ip_idx+=1
        nextline = 0
ip_idx = 0
IPaddresses = outstr.strip()

## Get the external IP address of this machine (actually, the router's) 
extIPaddressresult = subprocess.run(['/usr/bin/dig','+short','myip.opendns.com','@resolver1.opendns.com'], stdout=subprocess.PIPE)
extIPaddress = extIPaddressresult.stdout.decode('UTF-8').strip()

# File in which to store the relevant information
fname = 'ipaddress_'+hostname+'.txt'
fpath =  homedir+'/.ipdisclose/'+fname
refresh = True
# Check that the file exists
if os.path.isfile(fpath):
    f=open(fpath,"r")
    iplines = f.readlines()
    f.close()
    old_ip[0] = iplines[3].split()[1]
    old_ip[1] = iplines[4].split()[1]
    old_ip[2] = iplines[5]
    # Check to see if there have been any changes
    refresh = ((old_ip[0] != current_ip[0]) or (old_ip[1] != current_ip[1]) or (old_ip[2] != extIPaddress))
# If the file didn't exist, or if there have been changes
if refresh:
    # Write it all to the file
    f=open(fpath,"w")
    f.write(hostname+"\n")
    f.write(readingDate+"\n")
    f.write(readingTime+"\n")
    f.write(IPaddresses+"\n")
    f.write(extIPaddress)
    f.truncate()
    f.close()
    # Send the file to the public webserver
    # Get the credentials
    with open('epizyftp.json') as json_credentials_file:
        credentials = json.load(json_credentials_file)
    remotehost = credentials['FTP']['FTP_SERVER']
    username = credentials['FTP']['FTP_USER']
    password = credentials['FTP']['FTP_PASSWD']
    # Establish a connection and send the file
    ftp = FTP(host=remotehost,user=username,passwd=password)
    ftp.cwd("/htdocs/rpis")
    with open(fpath, 'rb') as f:
       ftp.storbinary('STOR '+fname, f)
    ftp.quit()

