#!/usr/bin/env python3

from ftplib import FTP

import project_data, paramiko

with FTP(host='ftp.example.com', user='me', passwd='secret') as ftp:
    print(ftp.getwelcome())

# Define SFTP connection parameters
hostname = project_data.FTP_HOST
port = 22
username = 'your_username'
password = 'your_password'

# Create an SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SFTP server
ssh_client.connect(hostname, port, username, password)

# Create an SFTP session
sftp = ssh_client.open_sftp()

# Now you can perform SFTP operations

local_file = '/path/to/local/file.txt'
remote_file = '/path/to/remote/file.txt'
sftp.put(local_file, remote_file)