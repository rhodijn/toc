#!/usr/bin/env python3

import os, paramiko, project_data, re

files_local = []
files_remote = []

def find_toc(files_local, path):
    files_local = sorted(os.listdir(path))

    for f in files_local:
        if not re.search('^\\d+.pdf', f):
            files_local.remove(f)
    
    print('files to process: ', end='')
    print(files_local)

    return files_local

def upload_toc(files_local):
    host_name = project_data.FTP_HOST
    port = project_data.FTP_PORT
    user_name = project_data.USER
    p_word = project_data.PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host_name, port=port, username=user_name, password=p_word, look_for_keys=False)

    sftp_client = ssh_client.open_sftp()
    print("connection established ... ")

    files_remote = sftp_client.listdir(project_data.P_REMOTE)

    for f in files_local:
        if f in files_remote:
            print('file ' + f  + ' is already online')
            continue
        try:
            sftp_client.put(project_data.P_LOCAL + f, project_data.P_REMOTE + f)
            print('file uploaded: ' + f)
        except OSError as e:
            print(e)

    print(f'remote files: {sftp_client.listdir(project_data.P_REMOTE)}')

    sftp_client.close()
    ssh_client.close()

def move_toc(files_local):
    for f in files_local:
        os.rename(project_data.P_LOCAL + f, project_data.P_ARCHIVE + f)
    
    files_local = find_toc(files_local, project_data.P_LOCAL)

    return files_local

if __name__ == '__main__':
    files_local = find_toc(files_local, project_data.P_LOCAL)
    upload_toc(files_local)
    files_local = move_toc(files_local)