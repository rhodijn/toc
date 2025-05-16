#!/usr/bin/env python3

#======================================================================
# add 856 field to a record in alma
# version 0.1, 2025-05-16
#
# useage of command line tool:
#
# created by rhodijn for zhaw hsb, cc-by-sa
#======================================================================


import argparse, datetime, json, os, paramiko, project_data, re

finished = False

def get_record(finished: bool) -> tuple:
    """
    get path to toc file from input

    returns:
    args.file: str = path to to file
    """
    
    for key, value in log:
        f_process = {}

    try:
        with open(project_data.P_LOG + f_log, mode='r', encoding='utf-8') as f:
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

    return mms_id, url, finished


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
    while not finished:
        mms_id, url, finished = get_record(finished)
        print()