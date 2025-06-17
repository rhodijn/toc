#!/usr/bin/env python3
#
#   ###################     this is the main routine
#   ##                 ##   version 1.0 (2025-06-17)
#   ##               ##
#     ######       ##       python enrich.py -f toc/local/BM2064158.pdf -l win
#       ##       ######
#     ##               ##   created by rhodijn (zolo) for zhaw hsb
#   ##                 ##   without the help of ai
#     ###################   licensed under the apache license, version 2.0
#
#===============================================================================


import datetime, json, sys
sys.path.append('modules/')

from dotenv import dotenv_values
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
    this is the main routine, it controls the entire workflow
    """
    log = load_json(f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')
    args = get_args()
    barcode = args.file.split('/')[-1].split('.')[0].upper()

    # check if the toc of the item has already been processed
    if barcode in log.keys():
        processing = log[barcode]
        if log[barcode]['added_856']:
            processing['messages'].append('toc already processed')
    else:
        processing = load_json('log.json', 'd')

    processing.update({'dt': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    processing['filename'].update({'local': args.file.split('/')[-1]})

    # check if a valid file was submitted
    valid_file, msg = check_file(args.file)
    processing['messages'].append(msg)

    if valid_file:
        processing['valid'].update({'file': True})
        # check if a valid library was submitted
        valid_lib, msg = check_lib(args.lib.lower())
        processing['messages'].append(msg)

        if valid_lib:
            processing['valid'].update({'lib': True})

            # get the mms-id (iz) based on the barcode
            req, get_iz_mmsid = api_request('get', barcode, 'j', 'items?item_barcode=')
            processing['requests'].append(req)
            data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

            mmsid_iz = data['bib_data']['mms_id']
            processing['mms_id'].update({'iz': mmsid_iz})
            processing['messages'].append('iz mms-id retrieved')

            # get the mms-id (nz) based on the mms-id (iz)
            req, get_nz_mmsid = api_request('get', mmsid_iz, 'j', 'bibs/', config["api"]["get"])
            processing['requests'].append(req)
            data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

            try:
                mmsid_nz = data['linked_record_id']['value']
            except Exception as e:
                processing['messages'].append(f"error: {e}")

            if data['linked_record_id']['type'].upper() == 'NZ':
                processing['mms_id'].update({'nz': mmsid_nz})
                processing['messages'].append('nz mms-id retrieved')

                # upload the pdf-file to the server
                processing = upload_pdf(processing, args.file, args.lib.lower())
                # test the generated url
                processing = check_url(processing)
                # remove the local file
                processing = rm_file(processing, args.file)

                if processing['link_tested']:
                    req, get_iz_record = api_request('get', processing['mms_id']['iz'], 'x', 'bibs/', config['api']['get'])
                    data_xml = get_iz_record.content.decode(encoding='utf-8')

                    # save the bibliographic record retrieved from alma
                    save_to_xml(processing, data_xml)

                    if processing['xml_saved']:
                        # add the field 856
                        processing = add_856_field(processing)

                        # update the bibliographic record in alma (including the added field)
                        req, record_updated = api_request('put', processing['mms_id']['iz'], 'x', 'bibs/', config["api"]["put"])
                        processing['requests'].append(req)

                        if record_updated:
                            processing.update({'put_request': True})
                            processing['messages'].append('alma record updated')
                        else:
                            processing['messages'].append('put request failed')
            else:
                processing['messages'].append('nz mms-id not found')

    log.update({barcode: processing})

    # write the log-data to the log file
    success = write_json(log, f"log_{datetime.datetime.now().strftime('%Y')}.json", 'l')

    # send the enrichment report e-mail
    send_email(barcode, processing)