#!/usr/bin/env python3

# ======================================================================
# this script reads the barcode from the filename.
# it then finds the nz mms-id by performing get requests.
# version 0.1, 2025-05-22
#
# [°_°]
# created by rhodijn for zhaw hsb, cc-by-sa
# ======================================================================


from lxml import etree
from project_data import *
import json, os, requests

mmsid_iz = 9947393580105520
mmsid_nz = 991017945329705501
url = f'https://{FTP_HOST}/public/swisscovery/inhaltsverzeichnis/winterthur/{mmsid_iz}.pdf'

file_list = os.listdir('toc/local')
barcodes = []

for el in file_list:
    barcodes.append(el.split('.')[0].upper())

get_iz_mmsid = requests.get(f'{API_URL}items?item_barcode={barcodes[0]}&apikey={API_KEY}&format={API_FRMT["j"]}')

data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

for key in data.keys():
    print(key)

mmsid_iz = data['bib_data']['mms_id']

get_nz_mmsid = requests.get(f'{API_URL}bibs/{mmsid_iz}{API_PARA_GET}&apikey={API_KEY}&format={API_FRMT["j"]}')

data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

print(data['mms_id'])

if data['linked_record_id']['type'].upper() == 'NZ':
    print(data['linked_record_id']['value'])

os.rename(f'toc/local/{barcodes[0]}.pdf', f'toc/local/{data["linked_record_id"]["value"]}.pdf')