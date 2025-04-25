#!/usr/bin/env python3

import os, paramiko, project_data, re

f_processed = {}

def find_toc(f_processed, path):
    f_local = []
    f_local = sorted(os.listdir(path))

    for f in f_local:
        if re.search ('^\\d+.pdf', f):
            f_processed.update({f: False})
        else:
            os.rename(project_data.P_TOC + f, project_data.P_TRASH + f)
    
    print(f'local files: {[f for f in f_processed.keys()]}')

    return f_processed

def upload_toc(f_processed):
    f_remote = []
    host_name = project_data.FTP_HOST
    port = project_data.FTP_PORT
    user_name = project_data.USER
    p_word = project_data.PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host_name, port=port, username=user_name, password=p_word, look_for_keys=False)

    sftp_client = ssh_client.open_sftp()
    print("connection established ... ")

    f_remote = sftp_client.listdir(project_data.P_REMOTE + project_data.P_WIN)

    for f in f_processed.keys():
        if f in f_remote:
            print('file ' + f + ' already online (will not be replaced)')
            continue
        try:
            sftp_client.put(project_data.P_TOC + f, project_data.P_REMOTE + project_data.P_WIN + f)
            f_processed[f] = True
        except Exception as e:
            print(e)

    f_remote = sftp_client.listdir(project_data.P_REMOTE + project_data.P_WIN)

    print(f'files uploaded: {[f for f in f_processed.keys() if f_processed[f] == True]}')
    print(f'remote files: {f_remote}')

    sftp_client.close()
    ssh_client.close()

    return f_processed

def move_toc(f_processed):
    for f in f_processed.keys():
        if f_processed[f]:
            os.rename(project_data.P_TOC + f, project_data.P_DONE + f)
        else:
            os.rename(project_data.P_TOC + f, project_data.P_NOT + f)

    return f_processed

if __name__ == '__main__':
    f_processed = find_toc(f_processed, project_data.P_TOC)
    f_processed = upload_toc(f_processed)
    f_processed = move_toc(f_processed)