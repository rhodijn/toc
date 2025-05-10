#!/usr/bin/env python3

#----------------------------------------------------------------------
# command line tool to upload a toc-file to server
# version 0.1, 2025-05-08
#
# useage of command line tool:
#
# python upload.py -f toc/123.pdf -l win
# python upload.py --file toc/123.pdf --lib win
# python3 upload.py -f toc/123.pdf -l win
# python3 upload.py --file toc/123.pdf --lib win
#
# created by rhodijn for zhaw hsb, cc-by-sa
#----------------------------------------------------------------------

# NEXT FEATURES:
# instead of p_local and f_name, reduce do one variable
# or separate path from file name

import argparse, datetime, json, os, paramiko, project_data, re

def get_file():
    """
    Get path to toc file from input

    Returns:
    args.file: str = path to to file
    """
    parser = argparse.ArgumentParser(
        prog = 'toc uploader',
        description = 'upload toc to ftp-server from terminal',
        epilog = 'zhaw hsb, cc-by-sa'
    )

    parser.add_argument('-f', '--file', required=True, type=str, help='path to and name of toc file')
    parser.add_argument('-l', '--lib', required=True, type=str, help='library, used for remote path')

    args = parser.parse_args()

    return args

def check_toc(p_local: str) -> tuple:
    """
    Collect files for upload to remote server

    Parameters:
    p_local: str = relative path to toc-file

    Returns:
    f_process: dict = {file name: dict = {}}
    """
    f_process = {}
    f_name = p_local.split('/')[-1]

    f_process.update(
        {
            f_name: {
                'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'filename': f_name,
                'valid': False,
                'upload': False,
                'deleted': False,
                'messages': [],
                'url': None, 
                'mms-id': None
            }
        }
    )

    if re.search('\\b\\d{13,23}\\.(pdf|PDF)\\b', f_name):
        f_process[f_name].update(
            {
                'valid': True,
                'mms-id': int(re.search('\\b\\d{13,23}', f_name).group())
            }
        )
    elif re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f_name):
        f_process[f_name]['messages'].append('file not pdf format')
    elif re.search('\\b\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f_name):
        f_process[f_name]['messages'].append('non-digit characters in file name')
    else:
        f_process[f_name]['messages'].append('error of another kind')

    return f_process, f_name

def upload_toc(f_process: dict, f_name: str, p_local: str, p_bib: str) -> dict:
    """
    Upload collected file to remote server (only pdf not already online)

    Parameters:
    f_process: dict = {file name: dict = {}}
    f_name: str = name of the file
    p_local: str = path to local file
    p_bib: str = remote path to files of library (winterthur or waedenswil)

    Returns:
    f_process: dict = {file name: dict = {}}
    """
    f_remote : list = []
    host_name : str = project_data.FTP_HOST
    port : int = project_data.FTP_PORT
    user_name : str = project_data.FTP_USR
    p_word : str = project_data.FTP_PWD

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=host_name,
        port=port,
        username=user_name,
        password=p_word,
        look_for_keys=False
    )

    sftp_client = ssh_client.open_sftp()

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)
    
    if f_name in f_remote:
        f_process[f_name]['messages'].append('file already online')
    else:
        try:
            sftp_client.put(p_local, project_data.P_REMOTE + p_bib + f_process[f_name]['filename'])
            url = f'https://{project_data.FTP_HOST}/{project_data.P_REMOTE}{project_data.P_WIN}{f_name}'
            f_process[f_name].update({'upload': True, 'url': url})
            f_process[f_name]['messages'].append('upload successful')
        except Exception as e:
            f_process[f_name]['messages'].append(f'error {e} occurred')

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)

    sftp_client.close()
    ssh_client.close()

    return f_process

def rm_toc(f_process: dict, f_name: str, p_local: str) -> dict:
    """
    Delete local file

    Parameters:
    f_process: dict = {file name: dict = {}}
    f_name: str = name of the file
    p_local: str = path to local file

    Returns:
    f_process: dict = {file name: dict = {}}
    """
    if os.path.exists(p_local):
        os.remove(p_local)
        f_process[f_name].update({'deleted': True})
        f_process[f_name]['messages'].append('local file removed')
    else:
        f_process[f_name]['messages'].append('file not found')

    return f_process

def write_json(f_process: dict, p_log: str, f_name: str) -> dict:
    """
    Save result to a json log file

    Parameters:
    f_process: dict = {file name: dict = {}}
    p_log: str = path to log-file
    f_name: str = name of json log-file

    Returns:
    f_process: dict = {file name: dict = {}}
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
    args = get_file()
    if not re.search('\\bw[ai][en]\\b', args.lib.lower()):
        print('please specify a valid library')
    else:
        f_process, f_name = check_toc(args.file)
        if not f_process[f_name]['valid']:
            print('please submit a valid file')
        else:
            f_process = upload_toc(f_process, f_name, args.file, project_data.P_LIB[args.lib.lower()])
            f_process = rm_toc(f_process, f_name, args.file)
            f_process = write_json(
                f_process, project_data.P_LOG,
                f'toc_log_{datetime.datetime.now().strftime("%Y")}.json'
            )