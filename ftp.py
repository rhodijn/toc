#!/usr/bin/env python3

import os, paramiko, project_data, re

f_processed : dict = {}

def find_toc(f_processed, p_local):
    """
    Collect files for upload to remote server

    Parameters:
    f_processed : dict = {file names : str: processed : bool}
    p_local : str = relative local path to toc-files

    Returns:
    f_processed : dict = {file names : str: processed : bool}
    """
    f_local : list = []
    f_local = sorted(os.listdir(p_local))

    for f in f_local:
        if re.search ('^\\d+.pdf', f):
            f_processed.update({f: False})
        else:
            os.rename(p_local + f, project_data.P_TRASH + f)
            print('file ' + f + ' cannot be processed')
    
    print(f'local files: {[f for f in f_processed.keys()]}')

    return f_processed

def upload_toc(f_processed, p_bib):
    """
    Upload collected files to remote server (only pdfs not already online)

    Parameters:
    f_processed : dict = {file names : str: processed : bool}
    p_bib : str = remote path to files of library (winterthur or waedenswil)

    Returns:
    f_processed : dict = {file names : str: processed : bool}
    """
    f_remote : list = []
    host_name : str = project_data.FTP_HOST
    port : int = project_data.FTP_PORT
    user_name : str = project_data.FTP_USR
    p_word : str = project_data.FTP_PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host_name, port=port, username=user_name, password=p_word, look_for_keys=False)

    sftp_client = ssh_client.open_sftp()
    print('connection established')

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)

    for f in f_processed.keys():
        if f in f_remote:
            print('file ' + f + ' not replaced (already online)')
            continue
        try:
            sftp_client.put(project_data.P_TOC + f, project_data.P_REMOTE + p_bib + f)
            f_processed[f] = True
            print('file ' + f + ' uploaded')
        except Exception as e:
            print('an error occurred: ' + e)

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)

    print(f'files uploaded: {[f for f in f_processed.keys() if f_processed[f]]}')
    print(f'remote files: {f_remote}')

    sftp_client.close()
    ssh_client.close()

    return f_processed

def move_toc(f_processed):
    """
    Move local files to done-, not- or trash-folder

    Parameters:
    f_processed : dict = {file names : str: processed : bool}

    Returns:
    f_processed : dict = {file names : str: processed : bool}
    """
    for f in f_processed.keys():
        if f_processed[f]:
            os.rename(project_data.P_TOC + f, project_data.P_DONE + f)
        else:
            os.rename(project_data.P_TOC + f, project_data.P_NOT + f)

    return f_processed

if __name__ == '__main__':
    f_processed = find_toc(f_processed, project_data.P_TOC)
    f_processed = upload_toc(f_processed, project_data.P_WIN)
    f_processed = move_toc(f_processed)