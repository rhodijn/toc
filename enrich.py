#!/usr/bin/env python3
#
#   ###################      this is the main routine
#   ##                 ##    version 0.7 (2025-06-02)
#   ##               ##
#     ######       ##        python enrich.py -f toc/local/BM2064158.pdf -l win
#       ##       ######
#     ##               ##    created by rhodijn (zolo) for zhaw hsb
#   ##                 ##
#     ###################    licensed under the apache license, version 2.0
#
#===============================================================================


import datetime, json, os, sys
sys.path.append('modules/')

from dotenv import dotenv_values
from lxml import etree
from modules.apihandler import *
from modules.checker import *
from modules.logger import *
from modules.mailer import *
from modules.uploader import *
from modules.xmlhandler import *


config = load_json('config.json', 'd')
secrets = dotenv_values('.env')
processing = {}
log = {}


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the entire workflow
    """
    log = load_json(f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')
    args = get_args()
    barcode = args.file.split('/')[-1].split('.')[0].upper()

    if barcode in log.keys():
        processing = log[barcode]
        if log[barcode]['added_856']:
            processing['messages'].append('toc already processed')
    else:
        processing = load_json('log.json', 'd')
        
    processing.update({'dt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    processing['filename'].update({'local': args.file.split('/')[-1]})

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
            processing['mms_id'].update({'iz': mmsid_iz})
            processing['messages'].append('iz mms-id retrieved')

            req, get_nz_mmsid = api_request('get', mmsid_iz, 'bibs/', config["api"]["get"])
            processing['requests'].append(req)
            data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

            try:
                mmsid_nz = data['linked_record_id']['value']
            except Exception as e:
                processing['messages'].append(f"error: {e}")

            if data['linked_record_id']['type'].upper() == 'NZ':
                processing['mms_id'].update({'nz': mmsid_nz})
                processing['messages'].append('nz mms-id retrieved')
                processing = upload_pdf(processing, args.file, args.lib.lower())
                processing = check_url(processing)
                processing = rm_file(processing, args.file)

                if processing['link_tested']:
                    req, get_iz_record = api_request('get', processing['mms_id']['iz'], 'bibs/', config['api']['get'])
                    data_json = json.loads(get_iz_record.content.decode(encoding='utf-8'))
                    success = write_json(data_json, f"{data_json['mms_id']}.json", 't')

                    if success:
                        processing = json_to_xml(processing, data_json)

                        if processing['xml_saved']:
                            processing = add_856_field(processing, data_json)

            else:
                processing['messages'].append('nz mms-id not found')

    log.update({barcode: processing})
    success = write_json(log, f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')

    send_email(barcode, processing)