#!/usr/bin/env python3
#
#   ##################      this module handles the upload
#   ##                ##    version 0.1 (2025-05-23)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import paramiko

from dotenv import dotenv_values
from logger import *


secrets = dotenv_values('.env')


def send_mail(f_process: dict, f_toc: str, p_bib: str, para_file: str) -> dict:
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
    config = load_json('config.json', 'd')
    mms_id = f_toc.split('.')[0]
    f_remote : list = []

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=secrets['FTP_URL'],
        port=config['ftp']['port'],
        username=secrets['FTP_USER'],
        password=secrets['FTP_PASS'],
        look_for_keys=False
    )

    sftp_client = ssh_client.open_sftp()

    f_remote = sftp_client.listdir(config['path']['r'] + p_bib)
    
    if f_toc in f_remote:
        f_process[mms_id]['messages'].append('file already online')
    else:
        try:
            sftp_client.put(para_file, config['path']['r'] + p_bib + f_process[mms_id]['filename'])
            url = f"{secrets['FTP_URL']}/{config['path']['r']}{p_bib}{f_toc}"
            f_process[mms_id].update({'uploaded': True, 'url': url})
            f_process[mms_id]['messages'].append('upload successful')
        except Exception as e:
            f_process[mms_id]['messages'].append(f"error: {e} occurred")

    f_remote = sftp_client.listdir(config['path']['r'] + p_bib)

    sftp_client.close()
    ssh_client.close()

    return f_process