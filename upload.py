#!/usr/bin/env python3

import argparse, datetime, json, os, paramiko, project_data, re

f_processed : dict = {}

def check_toc(f_processed, p_local):
    """
    Collect files for upload to remote server

    Parameters:
    f_processed : dict = {file names : str: processed : bool}
    p_local : str = relative local path to toc-files

    Returns:
    f_processed : dict = {file names : str: processed : bool}
    """
    f_name = re.search('[^\/]\w+\.\w{2,5}', p_local).group()
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f_processed.update({f_name: {'dt': dt, 'filename': f_name, 'status': False, 'message': None, 'url': None, 'mms-id': None}})

    if re.search('\\b\\d{13,23}\\.(pdf|PDF)\\b', f_name):
        f_processed[f_name].update({'status': True, 'mms-id': int(re.search('\\b\\d{13,23}', f_name).group())})
    elif re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f_name):
        f_processed[f_name].update({'message': 'file not pdf format'})
    elif re.search('\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f_name):
        f_processed[f_name].update({'message': 'non-digit characters in file name'})
    else:
        f_processed[f_name].update({'message': 'error of another kind'})

    return f_processed

def upload_toc(f_processed, p_local, p_bib):
    """
    Upload collected files to remote server (only pdfs not already online)

    Parameters:
    f_processed : dict = {file name : dict = {}}
    p_bib : str = remote path to files of library (winterthur or waedenswil)

    Returns:
    f_processed : dict = {file name : dict = {}}
    """
    f_name = f_processed[list(f_processed)[0]]['filename']
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
    
    if f_name in f_remote:
        f_processed[f_name].update({'message': 'already online'})
        print(f'file {f_name} already on server')
    else:
        try:
            sftp_client.put(p_local, project_data.P_REMOTE + p_bib + f_processed[f_name]['filename'])
            url = f'https://{project_data.FTP_HOST}/{project_data.P_REMOTE}{project_data.P_WIN}{f_name}'
            f_processed[f_name].update({'status': True, 'message': 'upload successful', 'url': url})
        except Exception as e:
            f_processed[f_name].update({'message': f'error {e}'})
            print(f'an error ({e}) occurred while processing {f_name}')

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

def write_json(f_processed, p_log, f_name):
    """
    Save result to a json log file

    Parameters:
    f_processed : dict = {file name : dict = {}}
    p_log : str = path to log-file
    f_name : str = name of json log-file

    Returns:
    f_processed : dict = {file name : dict = {}}
    """
    log = {}

    try:
        with open(p_log + f_name, mode='r', encoding='utf-8') as f:
            log = json.load(f)
    except:
        print(f'file {f_name} does not exist')

    log.update(f_processed)

    with open(p_log + f_name, mode='w', encoding='utf-8') as f:
        f.seek(0)
        json.dump(log, f, indent=4)

    return f_processed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="upload toc to ftp-server from terminal"
    )
    parser.add_argument("--file", required=True, type=str)
    args = parser.parse_args()

    p_local = args.file
    
    f_processed = check_toc(f_processed, p_local)
    f_processed = upload_toc(f_processed, p_local, project_data.P_WIN)
    print(f_processed)
    # f_processed = move_toc(f_processed)
    # f_processed = write_json(f_processed, project_data.P_LOG, 'toc_log.json')