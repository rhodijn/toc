#!/usr/bin/env python3

import argparse, datetime, json, os, paramiko, project_data, re

f_process : dict = {}

def get_file():
    parser = argparse.ArgumentParser(
        prog = 'toc uploader',
        description = 'upload toc to ftp-server from terminal',
        epilog = 'zhaw hsb, cc-by-sa'
    )
    parser.add_argument('-f', '--file', required=True, type=str)
    args = parser.parse_args()

    return args.file

def check_toc(f_process, p_local):
    """
    Collect files for upload to remote server

    Parameters:
    f_process : dict = {file names : str: processed : bool}
    p_local : str = relative local path to toc-files

    Returns:
    f_process : dict = {file names : str: processed : bool}
    """
    f_name = re.search('[^\/]\w+\.\w{2,5}', p_local).group()
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f_process.update({f_name: {'dt': dt, 'filename': f_name, 'valid': False, 'upload': False, 'moved': False, 'message': None, 'url': None, 'mms-id': None}})

    if re.search('\\b\\d{13,23}\\.(pdf|PDF)\\b', f_name):
        f_process[f_name].update({'valid': True, 'mms-id': int(re.search('\\b\\d{13,23}', f_name).group())})
    elif re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f_name):
        f_process[f_name].update({'message': 'file not pdf format'})
    elif re.search('\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f_name):
        f_process[f_name].update({'message': 'non-digit characters in file name'})
    else:
        f_process[f_name].update({'message': 'error of another kind'})

    return f_process

def upload_toc(f_process, f_name, p_local, p_bib):
    """
    Upload collected files to remote server (only pdfs not already online)

    Parameters:
    f_process : dict = {file name : dict = {}}
    p_bib : str = remote path to files of library (winterthur or waedenswil)

    Returns:
    f_process : dict = {file name : dict = {}}
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

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)
    
    if f_name in f_remote:
        f_process[f_name].update({'message': 'file already online'})
        print(f'file {f_name} already on server')
    else:
        try:
            sftp_client.put(p_local, project_data.P_REMOTE + p_bib + f_process[f_name]['filename'])
            url = f'https://{project_data.FTP_HOST}/{project_data.P_REMOTE}{project_data.P_WIN}{f_name}'
            f_process[f_name].update({'upload': True, 'message': 'upload successful', 'url': url})
        except Exception as e:
            f_process[f_name].update({'message': f'error {e} occurred'})

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)
    print(f'remote files: {f_remote}')

    sftp_client.close()
    ssh_client.close()

    return f_process

def move_toc(f_process, f_name, p_local):
    """
    Move local files to done-, not- or trash-folder

    Parameters:
    f_process : dict = {file name : dict = {}}

    Returns:
    f_process : dict = {file name : dict = {}}
    """
    try:
        if f_process[f_name]['upload']:
            os.rename(p_local, project_data.P_DONE + f_name)
        else:
            os.rename(p_local, project_data.P_NOT + f_name)

        f_process[f_name].update({'moved': True})
    except FileNotFoundError:
        f_process[f_name].update({'message': 'file not found'})

    return f_process

def write_json(f_process, p_log, f_name):
    """
    Save result to a json log file

    Parameters:
    f_process : dict = {file name : dict = {}}
    p_log : str = path to log-file
    f_name : str = name of json log-file

    Returns:
    f_process : dict = {file name : dict = {}}
    """
    log = {}

    try:
        with open(p_log + f_name, mode='r', encoding='utf-8') as f:
            log = json.load(f)
            log.update(f_process)
        with open(p_log + f_name, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(log, f, indent=4)
    except:
        with open(p_log + f_name, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(f_process, f, indent=4)

    return f_process

if __name__ == '__main__':
    p_local = get_file()
    f_process = check_toc(f_process, p_local)
    f_name = f_process[list(f_process)[0]]['filename']
    if f_process[f_name]['valid']:
        f_process = upload_toc(f_process, f_name, p_local, project_data.P_WIN)
    f_process = move_toc(f_process, f_name, p_local)
    f_process = write_json(f_process, project_data.P_LOG, 'toc_log.json')