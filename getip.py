#!/usr/bin/python3

# Get ip addresses
# script name: getip.py
# Peter Normington
# 2019-03-27

import datetime
import subprocess

from time import *

readingDateTime = datetime.datetime.now()
readingDate = str(readingDateTime.strftime("%Y-%m-%d"))
readingTime = str(readingDateTime.strftime("%H:%M:%S"))

hostresult = subprocess.run(['hostname'], stdout=subprocess.PIPE)
hostname = hostresult.stdout.decode('UTF-8')
fpath =  '/home/peter/Documents/ipaddress_'+hostname.strip()+'.txt'

outstr=""
ifcfgresult = subprocess.run(['ifconfig'], stdout=subprocess.PIPE)
ifcfg = ifcfgresult.stdout.decode('UTF-8')
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
            outstr+= line.split()[1]+"\n"
        else: outstr+="none\n"
        nextline = 0
f=open(fpath,"w")
f.write(hostname)
f.write(readingDate+"\n")
f.write(readingTime+"\n")
f.write(outstr)
f.close() 
