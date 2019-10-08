#!/usr/bin/python3

import json
from ftplib import FTP

# Get the credentials
with open('epizyftp.json') as json_credentials_file:
    credentials = json.load(json_credentials_file)
remotehost = credentials['FTP']['FTP_SERVER']
username = credentials['FTP']['FTP_USER']
password = credentials['FTP']['FTP_PASSWD']
print(remotehost)
print(username)
print(password)
# Establish a connection and list the "rpis" directory contents
ftp = FTP(host=remotehost,user=username,passwd=password)
ftp.cwd("/htdocs/rpis")
print(ftp.dir())
ftp.quit()