#!/usr/bin/env python3


################      this script gets the barcode from the filename
##              ##    it then finds the nz mms-id
##            ##
  ######    ##        version 0.4, 2025-05-22
    ##    ######
  ##            ##
##              ##
  ################    created by rhodijn for zhaw hsb, cc-by-sa [°_°]


from dotenv import load_dotenv
from project_data import *
import json, os, requests

load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
ftp_url = os.getenv('FTP_URL')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

mmsid_iz = 9947393580105520
mmsid_nz = 991017945329705501
url = f'{ftp_url}/{P_REMOTE}winterthur/{mmsid_iz}.pdf'
log = {}

file_list = os.listdir('toc/local')

for el in file_list:
    barcode = el.split('.')[0].upper()

    get_iz_mmsid = requests.get(f'{api_url}items?item_barcode={barcode}&apikey={api_key}&format={API_FRMT["j"]}')
    data = json.loads(get_iz_mmsid.content.decode(encoding='utf-8'))

    mmsid_iz = data['bib_data']['mms_id']
    get_nz_mmsid = requests.get(f'{api_url}bibs/{mmsid_iz}{API_PARA_GET}&apikey={api_key}&format={API_FRMT["j"]}')

    data = json.loads(get_nz_mmsid.content.decode(encoding='utf-8'))

    mmsid_nz = data["linked_record_id"]["value"]
    if data['linked_record_id']['type'].upper() == 'NZ':
        os.rename(f'{P_TOC}local/{barcode}.pdf', f'{P_TOC}local/{mmsid_nz}.pdf')
    else:
        print('mms-id not found')
    
    log.update({mmsid_nz: barcode})

print(log)