#!/usr/bin/env python3

import os, paramiko, project_data, re

file_list = []

def find_toc(file_list, path):
    file_list = sorted(os.listdir(path))

    for f in file_list:
        if not re.search('^\\d+.pdf', f):
            file_list.remove(f)

    return file_list

def upload_toc(file_list):
    host_name = project_data.FTP_HOST
    port = project_data.FTP_PORT
    user_name = project_data.USER
    p_word = project_data.PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host_name, port=port, username=user_name, password=p_word, look_for_keys=False)

    sftp_client = ssh_client.open_sftp()
    print("connection established ... ")

    print(f'remote files: {sftp_client.listdir(project_data.P_REMOTE)}')

    for f in file_list:
        try:
            sftp_client.put(str(project_data.P_LOCAL + f), str(project_data.P_REMOTE + f))
        except OSError as e:
            print(e)

    print(f'remote files: {sftp_client.listdir(project_data.P_REMOTE)}')

    sftp_client.close()
    ssh_client.close()

def move_toc(file_list):
    for f in file_list:
        os.rename(project_data.P_LOCAL + f, project_data.P_LOG + f)
    
    file_list = find_toc(file_list, project_data.P_LOCAL)

    return file_list

if __name__ == '__main__':
    file_list = find_toc(file_list, project_data.P_LOCAL)
    print(file_list)
    upload_toc(file_list)
    file_list = move_toc(file_list)
    print(file_list)