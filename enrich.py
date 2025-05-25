#!/usr/bin/env python3
#
#   ##################      this is the main routine
#   ##                ##    version 0.3 (2025-05-23)
#   ##              ##
#     ######      ##        python enrich.py -f toc/local/BM2064158.pdf -l win
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import datetime, json, sys
sys.path.append('modules/')

from dotenv import dotenv_values
from modules.apihandler import *
from modules.checker import *
from modules.logger import *
from modules.uploader import *


config = load_json('config.json', 'd')
secrets = dotenv_values('.env')
processing = {}
log = {}


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    log = load_json(f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')
    args = get_args()
    barcode = args.file.split('/')[-1].split('.')[0].upper()

    if barcode not in log.keys():
        processing = load_json('log.json', 'd')
        processing.update({'dt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
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

    req, get_iz_mmsid = api_request('get', barcode, 'items?item_barcode=')
    processing['requests'].append(req)
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

    mmsid_iz = data['bib_data']['mms_id']
    processing['mms-id'].update({'iz': mmsid_iz})
    processing['messages'].append('iz mms-id successfully retrieved')

    req, get_nz_mmsid = api_request('get', mmsid_iz, 'bibs/', config["api"]["get"])
    processing['requests'].append(req)
    data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

    try:
        mmsid_nz = data['linked_record_id']['value']
    except Exception as e:
        processing['messages'].append(f"error: {e}")

    if data['linked_record_id']['type'].upper() == 'NZ':
        processing['mms-id'].update({'nz': mmsid_nz})
        processing['messages'].append('nz mms-id successfully retrieved')
    else:
        processing['messages'].append('nz mms-id not found')

    log.update({barcode: processing})
    success = write_json(log, f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')