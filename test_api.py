#!/usr/bin/env python3

#======================================================================
# this script is for testing the alma api
# version 0.2, 2025-05-20
#
# created by rhodijn for zhaw hsb, cc-by-sa
#======================================================================

# next steps: alles holen mit GET, updaten, danach den gesamten Datensatz mit PUT wieder hochladen
# holen mit MMS-ID aus IZ, MMS-ID aus der NZ aus Datensatz extrahieren
# Barcode über API in Alma suchen und damit die MMS-ID holen?

from lxml import etree
import project_data, json, os, requests

mms_id = 9947393580105520
url = f'https://slspmedia.hsb.zhaw.ch/public/swisscovery/inhaltsverzeichnis/winterthur/{mms_id}.pdf'

get_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_GET}&apikey={project_data.API_KEY}&format={project_data.API_FRMT}'
print(f'GET REQUEST: {get_url}')

query = requests.get(get_url)

data_get = query.content.decode(encoding='utf-8')

with open('log/tmp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('log/tmp.xml')
xml_get = etree.tostring(tmp, pretty_print=True, encoding=str)

with open('log/get.xml', mode='w', encoding='utf-8') as f:
    f.write(xml_get)

os.remove('log/tmp.xml')

put_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_PUT}&apikey={project_data.API_KEY}'
print(f'PUT REQUEST: {put_url}')

query = requests.put(put_url, headers=project_data.API_HDR, data=f'{project_data.API_BDY_1}{url}{project_data.API_BDY_2}')

put_log = json.loads(query.content.decode('utf-8'))

with open('log/put_log.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(put_log, f, indent=4)