#!/usr/bin/env python3

import os, paramiko, project_data, pysftp, re

file_list = []

def find_toc(file_list):
    file_list = sorted(os.listdir(project_data.P_TOC))

    for f in file_list:
        if not re.search('^\\d+.pdf', f):
            file_list.remove(f)

    return file_list

def move_toc(file_list):
    host_name = project_data.FTP_HOST
    port = project_data.FTP_PORT
    user_name = project_data.USER
    p_word = project_data.PWD

    local_file = 'toc/' + file_list[0]
    remote_path = 'public/swisscovery/inthaltsverzeichnis/winterthur/'

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    with pysftp.Connection(host_name, port=port, username=user_name, password=p_word, cnopts=cnopts) as sftp:
        with sftp.cd(remote_path):
            sftp.put(local_file)

    print('Upload done.')

if __name__ == '__main__':
    file_list = find_toc(file_list)
    move_toc(file_list)