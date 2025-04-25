#!/usr/bin/env python3

import os, paramiko, project_data, re

f_local = []
f_processed = []
f_remote = []

def find_toc(f_local, path):
    f_local = sorted(os.listdir(path))

    for f in f_local:
        if not re.search('^\\d+.pdf', f):
            f_local.remove(f)
    
    print('local files to process: ', end='')
    print(f_local)

    return f_local

def upload_toc(f_local, f_remote):
    host_name = project_data.FTP_HOST
    port = project_data.FTP_PORT
    user_name = project_data.USER
    p_word = project_data.PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host_name, port=port, username=user_name, password=p_word, look_for_keys=False)

    sftp_client = ssh_client.open_sftp()
    print("connection established ... ")

    f_remote = sftp_client.listdir(project_data.P_REMOTE)

    for f in f_local:
        if f in f_remote:
            print('file ' + f  + ' is already online (will not be replaced)')
            continue
        try:
            sftp_client.put(project_data.P_LOCAL + f, project_data.P_REMOTE + f)
            f_processed.append(f)
        except OSError as e:
            print(e)

        print('files uploaded: ', end='')
        print(f_processed)

    print(f'remote files: {sftp_client.listdir(project_data.P_REMOTE)}')

    sftp_client.close()
    ssh_client.close()

    return f_local, f_remote

def move_toc(f_local, f_processed):
    for f in f_processed:
        os.rename(project_data.P_LOCAL + f, project_data.P_ARCHIVE + f)
    
    f_local = find_toc(f_local, project_data.P_LOCAL)

    return f_local, f_processed

if __name__ == '__main__':
    f_local = find_toc(f_local, project_data.P_LOCAL)
    f_local, f_remote = upload_toc(f_local, f_remote)
    f_local, f_processed = move_toc(f_local, f_processed)