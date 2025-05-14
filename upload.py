#!/usr/bin/env python3

#======================================================================
# command line tool to upload a toc-file to server
# version 0.5, 2025-05-12
#
# useage of command line tool:
#
# python upload.py -f toc/995860000000545470.pdf -l win
# python upload.py --file toc/995860000000545470.pdf --lib win
# python3 upload.py -f toc/995860000000545470.pdf -l win
# python3 upload.py --file toc/995860000000545470.pdf --lib win
#
# created by rhodijn for zhaw hsb, cc-by-sa
#======================================================================

# next steps: remove lines 218 - 224 (except from try/except)

import argparse, datetime, json, os, paramiko, project_data, re


def get_file():
    """
    get path to toc file from input

    returns:
    args.file: str = path to to file
    """
    parser = argparse.ArgumentParser(
        prog = 'toc uploader',
        description = 'upload toc to ftp-server from terminal',
        epilog = 'zhaw hsb, cc-by-sa'
    )

    parser.add_argument('-f', '--file', required=True, type=str, help='path to toc-file (including name)')
    parser.add_argument('-l', '--lib', required=True, type=str, help='library, used for remote path')

    args = parser.parse_args()

    return args


def check_toc(para_file: str, para_lib: str, p_log: str, f_log: str) -> tuple:
    """
    check if file for upload to remote server is valid

    parameters:
    para_file: str = clt parameter -f, path to toc-file (including name)
    para_lib: str = clt parameter -l, library
    p_log: str = path to log-file
    f_log: str = name of json log-file

    returns:
    f_process: dict = {file name: dict = {}}
    """
    f_process = {}
    f_toc = para_file.split('/')[-1]

    try:
        with open(p_log + f_log, mode='r', encoding='utf-8') as f:
            log = json.load(f)

    except:
        log = {}

        with open(p_log + f_log, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(log, f, indent=4)

    if f_toc in log.keys():
        f_process.update({f_toc: log[f_toc]})
        f_process[f_toc]['messages'].append(
            f'processed again: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
    else:
        f_process.update(
            {
                f_toc: {
                    'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'filename': f_toc,
                    'valid': {
                        'file': False,
                        'lib': False
                    },
                    'upload': False,
                    'deleted': False,
                    'messages': [],
                    'url': None, 
                    'mms-id': None
                }
            }
        )

    if re.search('\\b\\d{13,23}\\.(pdf|PDF)\\b', f_toc):
        f_process[f_toc].update(
            {
                'mms-id': int(re.search('\\b\\d{13,23}', f_toc).group())
            }
        )
        f_process[f_toc]['valid'].update(
            {
                'file': True
            }
        )
    elif re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f_toc):
        f_process[f_toc]['messages'].append('file not pdf format')
    elif re.search('\\b\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f_toc):
        f_process[f_toc]['messages'].append('non-digit characters in file name')
    else:
        f_process[f_toc]['messages'].append('error of another kind')

    if para_lib in project_data.P_LIB.keys():
        f_process[f_toc]['valid'].update(
            {
                'lib': True
            }
        )
    else:
        f_process[f_toc]['messages'].append(f'invalid parameter -l: {para_lib}')

    return f_process, f_toc, para_lib


def upload_toc(f_process: dict, f_toc: str, para_file: str, p_bib: str) -> dict:
    """
    upload collected file to remote server (only pdf not already online)

    parameters:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name
    para_file: str = path to local file
    p_bib: str = remote path to files of library (winterthur or waedenswil)

    returns:
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
    
    if f_toc in f_remote:
        f_process[f_toc]['messages'].append('file already online')
    else:
        try:
            sftp_client.put(para_file, project_data.P_REMOTE + p_bib + f_process[f_toc]['filename'])
            url = f'https://{project_data.FTP_HOST}/{project_data.P_REMOTE}{p_bib}{f_toc}'
            f_process[f_toc].update({'upload': True, 'url': url})
            f_process[f_toc]['messages'].append('upload successful')
        except Exception as e:
            f_process[f_toc]['messages'].append(f'error: {e} occurred')

    f_remote = sftp_client.listdir(project_data.P_REMOTE + p_bib)

    sftp_client.close()
    ssh_client.close()

    return f_process


def rm_toc(f_process: dict, f_toc: str, para_file: str) -> dict:
    """
    delete local file

    parameters:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name
    para_file: str = path to local file

    returns:
    f_process: dict = {file name: dict = {}}
    """
    if os.path.exists(para_file):
        os.remove(para_file)
        f_process[f_toc].update({'deleted': True})
        f_process[f_toc]['messages'].append('local file removed')
    else:
        f_process[f_toc]['messages'].append('file not found')

    return f_process


def write_json(f_process: dict, p_log: str, f_log: str) -> dict:
    """
    save result to a json log file

    parameters:
    f_process: dict = {file name: dict = {}}
    p_log: str = path to log-file
    f_log: str = name of json log-file

    returns:
    f_process: dict = {file name: dict = {}}
    """
    log = {}

    try:
        with open(p_log + f_log, mode='r', encoding='utf-8') as f:
            log = json.load(f)
            log.update(f_process)
        with open(p_log + f_log, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(log, f, indent=4)
    # das kann glaubs enfernt werden (ist nun im check_toc abgefangen)
    except:
        with open(p_log + f_log, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(f_process, f, indent=4)

    return f_process


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    args = get_file()
    f_process, f_toc, para_lib = check_toc(
        args.file,
        args.lib.lower(),
        project_data.P_LOG,
        f'log_{datetime.datetime.now().strftime("%Y")}.json'
    )
    if f_process[f_toc]['valid']['file'] and f_process[f_toc]['valid']['lib']:
        f_process = upload_toc(f_process, f_toc, args.file, project_data.P_LIB[para_lib])
    f_process = rm_toc(f_process, f_toc, args.file)
    f_process = write_json(
        f_process, project_data.P_LOG,
        f'log_{datetime.datetime.now().strftime("%Y")}.json'
    )