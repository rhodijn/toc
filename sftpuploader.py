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
        if re.search('\\b\\d{13,23}\\.(pdf|PDF)\\b', f):
            f_processed.update({f: {'dt': None, 'filename': f, 'status': False, 'message': None, 'url': None, 'mms-id': None}})
        else:
            if re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f):
                print(f'file {f} is not a pdf')
            elif re.search('\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f):
                print(f'file {f} uses non-digit characters in its name')
            else:
                print(f'file {f} not allowed for some other reason')
            os.rename(p_local + f, project_data.P_TRASH + f)
    
    print(f'local files: {[f for f in f_processed.keys()]}')

    return f_processed

def upload_toc(f_processed, p_bib):
    """
    Upload collected files to remote server (only pdfs not already online)

    Parameters:
    f_processed : dict = {file name : dict = {}}
    p_bib : str = remote path to files of library (winterthur or waedenswil)

    Returns:
    f_processed : dict = {file name : dict = {}}
    """
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            f_processed[f].update({'dt': dt, 'status': False, 'message': 'already online'})
            print(f'file {f} already on server')
            continue
        url = f'https://{project_data.FTP_HOST}/{project_data.P_REMOTE}{project_data.P_WIN}{f}'
        mms_id = int(re.search('\\b\\d{13,23}', f).group())
        try:
            sftp_client.put(project_data.P_TOC + f, project_data.P_REMOTE + p_bib + f.lower())
            f_processed[f].update({'dt': dt, 'status': True, 'message': 'upload successful', 'url': url, 'mms-id': mms_id})
        except Exception as e:
            f_processed[f].update({'dt': dt, 'status': False, 'message': f'error {e}'})
            print(f'an error ({e}) occurred while processing {f}')

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)
    print(f'remote files: {f_remote}')

    sftp_client.close()
    ssh_client.close()

    return f_processed

def move_toc(f_processed):
    """
    Move local files to done-, not- or trash-folder

    Parameters:
    f_processed : dict = {file name : dict = {}}

    Returns:
    f_processed : dict = {file name : dict = {}}
    """
    for f in f_processed.keys():
        if f_processed[f]:
            os.rename(project_data.P_TOC + f, project_data.P_DONE + f.lower())
        else:
            os.rename(project_data.P_TOC + f, project_data.P_NOT + f)

    return f_processed

def write_json(f_processed, f_path, f_name):
    """
    Save result to a json log file

    Parameters:
    f_processed : dict = {file name : dict = {}}
    f_path : str = path to log-file
    f_name : str = name of json log-file

    Returns:
    f_processed : dict = {file name : dict = {}}
    """
    log = {}

    try:
        with open(f_path + f_name, mode='r', encoding='utf-8') as f:
            log = json.load(f)
    except:
        print(f'file {f_name} does not exist')

    log.update(f_processed)

    with open(f_path + f_name, mode='w', encoding='utf-8') as f:
        f.seek(0)
        json.dump(log, f, indent=4)

    return f_processed

if __name__ == '__main__':
    f_processed = find_toc(f_processed, project_data.P_TOC)
    f_processed = upload_toc(f_processed, project_data.P_WIN)
    f_processed = move_toc(f_processed)
    f_processed = write_json(f_processed, project_data.P_LOG, 'toc_log.json')