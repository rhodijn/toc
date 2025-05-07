#!/usr/bin/env python3

import datetime, json, os, paramiko, project_data, re

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
        if re.search('\\b\\d{13,20}\\.(pdf|PDF)\\b', f):
            f_processed.update({f: {'dt': None, 'upload': False, 'message': None}})
        else:
            if re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f):
                print('file ' + f + ' is not a pdf')
            elif re.search('\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f):
                print('file ' + f + ' uses non-digit characters in its name')
            else:
                print('file ' + f + ' not allowed for some other reason')
            os.rename(p_local + f, project_data.P_TRASH + f)
    
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
            print('file ' + f + ' already on server')
            continue
        try:
            sftp_client.put(project_data.P_TOC + f, project_data.P_REMOTE + p_bib + f.lower())
            f_processed[f]['dt'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f_processed[f]['upload'] = True
        except Exception as e:
            print('an error (' + e + ') occurred while processing ' + f)

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)

    print(f'files uploaded: {[f.lower() for f in f_processed.keys() if f_processed[f]['upload']]}')
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
            os.rename(project_data.P_TOC + f, project_data.P_DONE + f.lower())
        else:
            os.rename(project_data.P_TOC + f, project_data.P_NOT + f)

    return f_processed

if __name__ == '__main__':
    f_processed = find_toc(f_processed, project_data.P_TOC)
    f_processed = upload_toc(f_processed, project_data.P_WIN)
    f_processed = move_toc(f_processed)

"""
def write_json_data(file_path, file_name, file_data):

    save data to a json file

    file_path : str = path to the json file
    file_name : str = name of the json file
    file_data : str = data to write to the file

    with open(file_path + file_name, mode='w', encoding='utf-8') as f:
        f.seek(0)
        json.dump(file_data, f, indent=4)

def read_json_data(file_path, file_name):

    read data from a json file

    file_path : str = path to the json file
    file_name : str = name of the json file

    try:
        with open(file_path + file_name, mode='r', encoding='utf-8') as f:
            file_data = json.load(f)
    except:
        return False
    return file_data

"""