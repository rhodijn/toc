#!/usr/bin/env python3

# ======================================================================
# this script is for testing the alma api
# version 0.2, 2025-05-20
#
# [°_°]
# created by rhodijn for zhaw hsb, cc-by-sa
# ======================================================================

# next steps: alles holen mit GET, updaten, danach den gesamten Datensatz mit PUT wieder hochladen
# holen mit MMS-ID aus IZ, MMS-ID aus der NZ aus Datensatz extrahieren
# Barcode über API in Alma suchen und damit die MMS-ID holen?

from lxml import etree
import project_data, json, os, requests

mmsid_iz = 9947393580105520
mmsid_nz = 991017945329705501
url = f'https://slspmedia.hsb.zhaw.ch/public/swisscovery/inhaltsverzeichnis/winterthur/{mmsid_iz}.pdf'

barcode = 'BM2064158'


# get record (xml)

get_url = f'{project_data.API_URL}{mmsid_iz}{project_data.API_PARA_GET}&apikey={project_data.API_KEY}&format={project_data.API_FRMT}'
print(f'RECORD GET REQUEST (XML): {get_url}')

query = requests.get(get_url)

data_get = query.content.decode(encoding='utf-8')

with open('log/temp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('log/temp.xml')
xml_get = etree.tostring(tmp, pretty_print=True, encoding=str)

with open('log/record.xml', mode='w', encoding='utf-8') as f:
    f.write(xml_get)

os.remove('log/temp.xml')


# get record (json)

get_url = f'{project_data.API_URL}{mmsid_iz}{project_data.API_PARA_GET}&apikey={project_data.API_KEY}&format=json'
print(f'RECORD GET REQUEST (JSON): {get_url}')

query = requests.get(get_url)

data_get = json.loads(query.content.decode(encoding='utf-8'))

with open('log/record.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(data_get, f, indent=4)


# get holdings

get_url = f'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs/{mmsid_nz}/holdings/ALL/items?limit=10&offset=0&order_by=none&direction=desc&view=brief&apikey={project_data.API_KEY}'
print(f'HOLDINGS GET REQUEST: {get_url}')

query = requests.get(get_url)

data_get = query.content.decode(encoding='utf-8')

with open('log/temp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('log/temp.xml')
xml_get = etree.tostring(tmp, pretty_print=True, encoding=str)

with open('log/holdings.xml', mode='w', encoding='utf-8') as f:
    f.write(xml_get)

os.remove('log/temp.xml')


# manipulate xml before putting

tree = etree.parse('log/record.xml')

root = tree.getroot()

add_tag = etree.fromstring(f'{project_data.API_BDY_1}{url}{project_data.API_BDY_2}')

for element in root.iter('datafield'):
    try:
        if int(element.attrib['tag']) <= 856:
            print(element.attrib)
        else:
            print(f'insert element here: {int(element.attrib["tag"])}')
    except:
        print('tag is not a number')

# Append new data
new_item = etree.SubElement(root[9], 'datafield')
new_item.attrib['tag'] = '856'
new_item.attrib['ind1'] = '4'
new_item.attrib['ind2'] = '2'


# put request

put_url = f'{project_data.API_URL}{mmsid_iz}{project_data.API_PARA_PUT}&apikey={project_data.API_KEY}'
print(f'PUT REQUEST: {put_url}')

query = requests.put(put_url, headers=project_data.API_HDR, data=etree.tostring(etree.parse('log/record_new.xml')))

if query.ok:
    print(query.text)
    print(query.headers)
    print(query.encoding)