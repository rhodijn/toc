#!/usr/bin/env python3

import os, paramiko, project_data, re

file_list = []

def find_toc(file_list):
    file_list = sorted(os.listdir(project_data.P_TOC))

    for f in file_list:
        if not re.search('^\\d+.pdf', f):
            file_list.remove(f)

    return file_list

def move_toc(file_list):
    hostname = project_data.FTP_HOST
    port = project_data.FTP_PORT
    username = project_data.USER
    password = project_data.PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(hostname, port, username, password)

    sftp = ssh_client.open_sftp()

    for f in file_list:
        local_file = '/toc/' + f
        remote_file = '/public/swisscovery/inthaltsverzeichnis/winterthur/' + f
        try:
            sftp.put(local_file, remote_file)
        except:
            print('some error')
            break
    else:
        print('all went well')
        

if __name__ == '__main__':
    file_list = find_toc(file_list)
    move_toc(file_list)