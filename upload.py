#!/usr/bin/env python3

# ======================================================================
# command line tool to upload a toc-file to server
# version 0.8, 2025-05-19
#
# useage of command line tool:
#
# python upload.py -f toc/995860000000545470.pdf -l win
# python upload.py --file toc/995860000000545470.pdf --lib win
# python3 upload.py -f toc/995860000000545470.pdf -l wae
# python3 upload.py --file toc/995860000000545470.pdf --lib wae
#
# [°_°]
# created by rhodijn for zhaw hsb, cc-by-sa
# ======================================================================

from project_data import *
import argparse, datetime, json, os, paramiko, re


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


def check_toc(p_log: str, f_log: str, para_file: str, para_lib: str) -> tuple:
    """
    check if file for upload to remote server is valid

    parameters:
    p_log: str = path to log-file
    f_log: str = name of json log-file
    para_file: str = clt parameter -f, path to toc-file (including name)
    para_lib: str = clt parameter -l, library

    returns:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name of toc
    para_lib: str = clt parameter -l, library
    """
    f_process = {}
    f_toc = para_file.split('/')[-1]
    mms_id = f_toc.split('.')[0]

    try:
        with open(p_log + f_log, mode='r', encoding='utf-8') as f:
            log = json.load(f)

    except:
        log = {}

        with open(p_log + f_log, mode='w', encoding='utf-8') as f:
            f.seek(0)
            json.dump(log, f, indent=4)

    if mms_id in log.keys():
        f_process.update({mms_id: log[mms_id]})
        f_process[mms_id]['messages'].append(
            f'processed again: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
    else:
        f_process.update(
            {
                mms_id: {
                    'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'filename': f_toc,
                    'valid': {
                        'file': False,
                        'lib': False
                    },
                    'uploaded': False,
                    'deleted': False,
                    'inserted': False,
                    'messages': [],
                    'url': None, 
                    'mms-id': None
                }
            }
        )

    if re.search('\\b99\\d{2,13}5501\\.(pdf|PDF)\\b', f_toc):
        f_process[mms_id].update(
            {
                'mms-id': int(mms_id)
            }
        )
        f_process[mms_id]['valid'].update(
            {
                'file': True
            }
        )
    elif re.search('(\\.(?!pdf|PDF))\\w{2,5}\\b', f_toc):
        f_process[mms_id]['messages'].append('file not pdf format')
    elif re.search('\\b\\d*[a-zA-Z]+\\d*\\.(pdf|PDF)\\b', f_toc):
        f_process[mms_id]['messages'].append('non-digit characters in file name')
    else:
        f_process[mms_id]['messages'].append('error of another kind')

    if para_lib in P_LIB.keys():
        f_process[mms_id]['valid'].update(
            {
                'lib': True
            }
        )
    else:
        f_process[mms_id]['messages'].append(f'invalid parameter -l: {para_lib}')

    return f_process, f_toc, para_lib


def upload_toc(f_process: dict, f_toc: str, p_bib: str, para_file: str) -> dict:
    """
    upload file to remote server (if pdf not already online)

    parameters:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name of toc
    p_bib: str = remote path to files of library (winterthur or waedenswil)
    para_file: str = path to local file

    returns:
    f_process: dict = {file name: dict = {}}
    """
    mms_id = f_toc.split('.')[0]
    f_remote : list = []
    host_name : str = FTP_HOST
    port : int = FTP_PORT
    user_name : str = FTP_USR
    p_word : str = FTP_PWD

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

    f_remote = sftp_client.listdir(P_REMOTE + p_bib)
    
    if f_toc in f_remote:
        f_process[mms_id]['messages'].append('file already online')
    else:
        try:
            sftp_client.put(para_file, P_REMOTE + p_bib + f_process[mms_id]['filename'])
            url = f'https://{FTP_HOST}/{P_REMOTE}{p_bib}{f_toc}'
            f_process[mms_id].update({'uploaded': True, 'url': url})
            f_process[mms_id]['messages'].append('upload successful')
        except Exception as e:
            f_process[mms_id]['messages'].append(f'error: {e} occurred')

    f_remote = sftp_client.listdir(P_REMOTE + p_bib)

    sftp_client.close()
    ssh_client.close()

    return f_process


def rm_toc(f_process: dict, f_toc: str, para_file: str) -> dict:
    """
    delete local file

    parameters:
    f_process: dict = {file name: dict = {}}
    f_toc: str = file name of toc
    para_file: str = path to local file

    returns:
    f_process: dict = {file name: dict = {}}
    """    
    mms_id = f_toc.split('.')[0]

    if os.path.exists(para_file):
        os.remove(para_file)
        f_process[mms_id].update({'deleted': True})
        f_process[mms_id]['messages'].append('local file removed')
    else:
        f_process[mms_id]['messages'].append('file not found')

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

    with open(p_log + f_log, mode='r', encoding='utf-8') as f:
        log = json.load(f)
        log.update(f_process)
    with open(p_log + f_log, mode='w', encoding='utf-8') as f:
        f.seek(0)
        json.dump(log, f, indent=4)

    return f_process


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    args = get_file()
    f_process, f_toc, para_lib = check_toc(
        P_LOG,
        f'log_{datetime.datetime.now().strftime("%Y")}.json',
        args.file,
        args.lib.lower()
    )
    mms_id = f_toc.split('.')[0]
    if f_process[mms_id]['valid']['file'] and f_process[mms_id]['valid']['lib']:
        f_process = upload_toc(f_process, f_toc, P_LIB[para_lib], args.file,)
    f_process = rm_toc(f_process, f_toc, args.file)
    f_process = write_json(
        f_process, P_LOG,
        f'log_{datetime.datetime.now().strftime("%Y")}.json'
    )