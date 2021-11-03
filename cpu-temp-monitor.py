#!/usr/bin/python3

# Script name: cpu-temp-monitor.py
# MONITOR THE CPU TEMP - on RPi4
# Peter Normington
# 2020-06-22

####################################################################

####################################################################

import datetime
import subprocess as sbpcss

from time import *


readingDateTime = datetime.datetime.now()
readingDate = str(readingDateTime.strftime("%Y-%m-%d"))
readingTime = str(readingDateTime.strftime("%H:%M:%S"))

# Get the home directory (eg "/home/dave")
userresult = sbpcss.run(['/usr/bin/whoami'], stdout=sbpcss.PIPE)
homedir = "/home/"+userresult.stdout.decode('UTF-8').strip()

## Get the CPU temperature 
CPUtemp = sbpcss.run(['/usr/bin/vcgencmd', 'measure_temp'], stdout=sbpcss.PIPE)
CPUt = CPUtemp.stdout.decode('UTF-8').strip()

# File in which to store the relevant information
fname = 'cputemp.txt'
fpath =  homedir+'/Documents/'+fname
# Write it all to the file
f=open(fpath,"a")
f.write(readingDate+" at ")
f.write(readingTime+": ")
f.write(CPUt+"\n")
f.truncate()
f.close()