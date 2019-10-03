#!/usr/bin/python3

# Script name: dig.py
# check external ip address
# Peter Normington
# 2019-08-30

import subprocess
import os

# Get the external IP address 
extIPaddressresult = subprocess.run(['/usr/bin/dig','+short','myip.opendns.com','@resolver1.opendns.com'], stdout=subprocess.PIPE)
extIPaddress = extIPaddressresult.stdout.decode('UTF-8').strip()

print(extIPaddress)

