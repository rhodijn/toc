#!/usr/bin/env python3
#
#   ###################      this script is for testing the alma api
#   ##                 ##    version 0.7 (2025-06-02)
#   ##               ##
#     ######       ##        python enrich.py -f toc/local/BM2064158.pdf -l win
#       ##       ######
#     ##               ##    created by rhodijn (zolo) for zhaw hsb
#   ##                 ##
#     ###################    licensed under the apache license, version 2.0
#
#===============================================================================


from lxml import etree
from project_data import *
import json, os, requests


mmsid_iz = 9947393580105520
mmsid_nz = 991017945329705501
url = f'{FTP_HOST}/{P_REMOTE}winterthur/{mmsid_iz}.pdf'

barcode = 'BM2064158'

file_list = os.listdir('temp/')

for f in file_list:
    print(f)

"""
# get record (xml)

get_url = f'{API_URL}bibs/{mmsid_iz}{API_PARA_GET}&apikey={API_KEY}&format={API_FRMT["x"]}'
print(f'RECORD GET REQUEST (XML): {get_url}')

query = requests.get(get_url)

data_get = query.content.decode(encoding='utf-8')

with open('temp/temp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('temp/temp.xml')
xml_get = etree.tostring(tmp, pretty_print=True, encoding=str)

with open('temp/record.xml', mode='w', encoding='utf-8') as f:
    f.write(xml_get)

# os.remove('temp/temp.xml')


# get record (json)

get_url = f'{API_URL}bibs/{mmsid_iz}{API_PARA_GET}&apikey={API_KEY}&format={API_FRMT["j"]}'
print(f'RECORD GET REQUEST (JSON): {get_url}')

query = requests.get(get_url)

data_get = json.loads(query.content.decode(encoding='utf-8'))

with open('temp/record.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(data_get, f, indent=4)


# get holdings

get_url = f'{API_URL}bibs/{mmsid_iz}/holdings/ALL/items?limit=10&offset=0&order_by=none&direction=desc&view=brief&apikey={API_KEY}'
print(f'HOLDINGS GET REQUEST: {get_url}')

query = requests.get(get_url)

data_get = query.content.decode(encoding='utf-8')

with open('temp/temp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('temp/temp.xml')
xml_get = etree.tostring(tmp, pretty_print=True, encoding=str)

with open('temp/holdings.xml', mode='w', encoding='utf-8') as f:
    f.write(xml_get)

# os.remove('temp/temp.xml')


# manipulate xml before putting

tree = etree.parse('temp/record.xml')

root = tree.getroot()

add_tag = etree.fromstring(f'{API_BDY_1}{url}{API_BDY_2}')

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

put_url = f'{API_URL}bibs/{mmsid_iz}{API_PARA_PUT}&apikey={API_KEY}'
print(f'PUT REQUEST: {put_url}')

query = requests.put(put_url, headers=API_HDR, data=etree.tostring(etree.parse('temp/record_new.xml')))

if query.ok:
    print(query.text)
    print(query.headers)
    print(query.encoding)
"""