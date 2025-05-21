#!/usr/bin/env python3

# ======================================================================
# add 856 field to a record in alma
# version 0.2, 2025-05-19
#
# [°_°]
# created by rhodijn for zhaw hsb, cc-by-sa
# ======================================================================


import datetime, json, os, project_data


def load_log(f_log: str) -> dict:
    """
    load logged data into a dictionary

    parameters:
    f_log: str = file name of log-file

    returns:
    log: dict = {file name: dict = {}}
    """
    if os.path.exists(f'{project_data.P_LOG}{f_log}'):
        with open(project_data.P_LOG + f_log, mode='r', encoding='utf-8') as f:
            log = json.load(f)
        return log
    else:
        return {}


def get_record() -> tuple:
    """
    get path to toc-file from input

    returns:
    mms_id: int = mms-id of record
    url: str = url to toc-file
    finished: bool = false if not all records have been processed
    log: dict = {file name: dict = {}}
    """
    for v in log.values():
        if v['uploaded'] and not v['inserted']:
            return v['mms-id'], v['url'], False, log

    return None, None, True, log


def insert_field(mms_id: int, url: str, log: dict) -> bool:
    api_body = f'{project_data.API_BDY_1}{log[str(mms_id)]["url"]}{project_data.API_BDY_2}'
    print(api_body)
    log[str(mms_id)].update({'inserted': True})
    log[str(mms_id)]['messages'].append('856 field added to record')
    return log


def write_json(log: dict, p_log: str, f_log: str):
    """
    save result to a json log-file

    parameters:
    log: dict = {file name: dict = {}}
    p_log: str = path to log-file
    f_log: str = name of json log-file

    returns:
    none
    """
    with open(p_log + f_log, mode='w', encoding='utf-8') as f:
        f.seek(0)
        json.dump(log, f, indent=4)


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    finished = False
    f_log = f'log_{datetime.datetime.now().strftime("%Y")}.json'
    log = load_log(f_log)

    if bool(log):
        while not finished:
            mms_id, url, finished, log = get_record()
            if mms_id:
                print(f'next record to update: {mms_id}')
                log = insert_field(mms_id, url, log)

        write_json(log, project_data.P_LOG, f_log)