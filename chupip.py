#!/usr/bin/python3

# Script name: chupip.py
# check and update ip address display
# Peter Normington
# 2019-04-07

###################################################################
# IMPORTANT: this file, together with the configuration           #
# file epizyftp.json, should be placed in a directory .ipdisclose #
# in the user's home directory.     The script is intended to     #
# be invoked by the cron daemon on startup (use @reboot with a    #
# suitable delay to ensure network connections are in place; for  #
# example "@reboot sleep 30 && /home/peter/.ipdisclose/chupip.py" #
###################################################################

import datetime
import subprocess
import os
import json

from time import *
from ftplib import FTP

readingDateTime = datetime.datetime.now()
readingDate = str(readingDateTime.strftime("%Y-%m-%d"))
readingTime = str(readingDateTime.strftime("%H:%M:%S"))

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
# Array variables for the IP addresses, wired and wireless
current_ip = ["",""]
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
IPaddresses = outstr.strip()

## Get the external IP address of this machine (actually, the router's) 
extIPaddressresult = subprocess.run(['/usr/bin/dig','+short','myip.opendns.com','@resolver1.opendns.com'], stdout=subprocess.PIPE)
extIPaddress = extIPaddressresult.stdout.decode('UTF-8').strip()

# File in which to store the relevant information
fname = 'ipaddress_'+hostname+'.txt'
fpath =  homedir+'/.ipdisclose/'+fname
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
with open(homedir+'/.ipdisclose/epizyftp.json') as json_credentials_file:
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

