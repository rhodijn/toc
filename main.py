#!/usr/bin/env python3
#
#   ##################      this is the main routine
#   ##                ##    version 0.3 (2025-05-23)
#   ##              ##
#     ######      ##        python main.py -f toc/local/BM2064158.pdf -l win
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import datetime, json, requests, sys
sys.path.append('modules/')

from dotenv import dotenv_values
from apihandler import *
from checker import *
from logger import *
from uploader import *


secrets = dotenv_values('.env')
processing = {}
log = {}


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """

    log = json_load(f'log_{datetime.datetime.now().strftime("%Y")}.json', 'l')
    args = get_args()
    barcode = args.file.split('/')[-1].split('.')[0].upper()

    if barcode not in log.keys():
        processing = json_load('log.json', 'd')
        processing.update({'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        processing['filename'].update({'local': args.file.split('/')[-1]})
    else:
        processing = log[barcode]

    valid_file, msg = check_file(args.file)
    processing['messages'].append(msg)

    if valid_file:
        processing['valid'].update({'file': True})
        valid_lib, msg = check_lib(args.lib.lower())
        processing['messages'].append(msg)

        if valid_lib:
            processing['valid'].update({'lib': True})

    log.update({barcode: processing})

    config = json_load('config.json', 'd')

    get_iz_mmsid = get_request(barcode)
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

    mmsid_iz = data['bib_data']['mms_id']
    log[barcode]['mms-id'].update({'iz': mmsid_iz})
    log[barcode]['messages'].append('iz mms-id found')
    get_nz_mmsid = requests.get(f'{config["api"]["url"]}bibs/{mmsid_iz}{config["api"]["get"]}&apikey={secrets["API_KEY"]}&format={config["api"]["j"]}')

    data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

    mmsid_nz = data['linked_record_id']['value']

    if data['linked_record_id']['type'].upper() == 'NZ':
        log[barcode]['mms-id'].update({'nz': mmsid_nz})
        log[barcode]['messages'].append('nz mms-id found')
        # os.rename(f'{P_TOC}local/{barcode}.pdf', f'{P_TOC}local/{mmsid_nz}.pdf')
    else:
        log[barcode]['messages'].append('nz mms-id not found')

    success = json_write(log, f'log_{datetime.datetime.now().strftime("%Y")}.json', 'l')