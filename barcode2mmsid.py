#!/usr/bin/env python3

# ======================================================================
# this script gets the barcode from the filename
# it then finds the nz mms-id by performing two get requests
# version 0.1, 2025-05-22
#
# [°_°]
# created by rhodijn for zhaw hsb, cc-by-sa
# ======================================================================


from project_data import *
import json, os, requests


mmsid_iz = 9947393580105520
mmsid_nz = 991017945329705501
url = f'https://{FTP_HOST}/{P_REMOTE}winterthur/{mmsid_iz}.pdf'

file_list = os.listdir('toc/local')

for el in file_list:
    barcode = el.split('.')[0].upper()

    get_iz_mmsid = requests.get(f'{API_URL}items?item_barcode={barcode}&apikey={API_KEY}&format={API_FRMT["j"]}')
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

    mmsid_iz = data['bib_data']['mms_id']
    get_nz_mmsid = requests.get(f'{API_URL}bibs/{mmsid_iz}{API_PARA_GET}&apikey={API_KEY}&format={API_FRMT["j"]}')

    data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

    if data['linked_record_id']['type'].upper() == 'NZ':
        os.rename(f'{P_TOC}local/{barcode}.pdf', f'{P_TOC}local/{data["linked_record_id"]["value"]}.pdf')
    else:
        print('mms-id not found')

print(file_list)