#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script name: c2.py
# check and update ip address display, based on chupip.py
# Peter Normington
# 2021-10-30
#
# Mark Bradley
# 2022-09-11
# Added logging and try - except loop around the ftp operation.
# 15 sec timeout added to ftp command.
#
# 
#
# This script requires the 'dig' command which is part of the
# dnsutils package. To check if this is installed type dig into
# the command line.  If the response is '# bash: dig: command not found'
# then run the following command to install it: sudo apt-get install dnsutils
#
# IMPORTANT: this file, together with the configuration
# file c2.json, should be placed in a directory .ipdisclose
# in the user's home directory.
# To create the .ipdisclose directory use the following command;
# mkdir .ipdisclose  NOTE the '.' makes this a hidden directory
#
# The script is intended to be invoked by the cron daemon on startup
# use @reboot with a suitable delay to ensure network connections are in place;
# for example '@reboot sleep 30 && /home/<your user name>/.ipdisclose/c2.py'
# use command crontab -e to edit the crontab file.
#
# The c2.py file must be executable by changing its properties
# see command chmod
#
# 
#################################################################################

import datetime
import subprocess
import json
import logging as lg

from time import *
from ftplib import FTP

# Logging configuration - log 'info' and above to file c2.log, fresh file for each run
lg.basicConfig(level=lg.INFO,filename='c2.log',filemode='w',
               format='%(asctime)s - %(levelname)s - %(message)s')

lg.info('IP data collection started')  # Write to log file.

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

# We need to find eth0 and wlan0.  Either one might not be present
eth0_exists = False
wlan0_exists = False
iflines = ifcfg.strip().split("\n")
for line in ifcfg.splitlines():
    line = line.strip()
    if line.startswith('eth0'):
        outstr+= ("eth0: ")
        nextline = 1
        eth0_exists = True
    elif line.startswith('wlan0'):
        if not(eth0_exists):
            outstr+=("eth0: No Wired connection\n")
        outstr+= ("wlan0: ")
        nextline = 1
        wlan0_exists = True
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
if "wlan0" not in IPaddresses:
    IPaddresses = IPaddresses + "\nNo WiFi card" 


## Get the external IP address of this machine (actually, the router's) 
extIPaddressresult = subprocess.run(['/usr/bin/dig','+short','myip.opendns.com','@resolver3.opendns.com'], stdout=subprocess.PIPE)
extIPaddress = extIPaddressresult.stdout.decode('UTF-8').strip()
lg.info('IP data collection completed')

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
lg.info(f'IP data written to file {fpath}')

# Send the file to the public webserver
# Get the credentials
# NOTE c2 requires 4 parameters in the json config file
with open(homedir+'/.ipdisclose/c2.json') as json_credentials_file:
    credentials = json.load(json_credentials_file)
remotehost = credentials['FTP']['FTP_SERVER']
username = credentials['FTP']['FTP_USER']
password = credentials['FTP']['FTP_PASSWD']
remotedir = credentials['FTP']['FTP_REMOTE_DIR'] # Need to contain "/htdocs/rpis"

# Establish a connection and send the file
lg.info(f'Start FTP to host:{remotehost}')
try:
    ftp = FTP(host=remotehost,user=username,passwd=password,timeout=15)
    ftp.cwd(remotedir)
    
    with open(fpath, 'rb') as f:
        ftp.storbinary('STOR '+fname, f)
    ftp.quit()
    lg.info('FTP completed')
    
except:   # In case of error log it.
    lg.exception('An Error Occured!')