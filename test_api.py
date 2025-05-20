#!/usr/bin/env python3

from lxml import etree
import project_data, json, os, requests

mms_id = 9947393580105520
url = 'https://slspmedia.hsb.zhaw.ch/public/swisscovery/inhaltsverzeichnis/winterthur/995860000000545473.pdf'

get_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_GET}&apikey={project_data.API_KEY}&format={project_data.API_FRMT}'

query = requests.get(get_url)

print(query)

data_get = query.content.decode(encoding='utf-8')

with open('log/tmp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_get)

tmp = etree.parse('log/tmp.xml')
xml_get = etree.tostring(tmp, pretty_print = True, encoding = str)

with open('log/get.xml', mode='w') as f:
    f.write(xml_get)

os.remove('log/tmp.xml')

put_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_PUT}&apikey={project_data.API_KEY}'

print(put_url)

query = requests.put(put_url, headers=project_data.API_HDR, data=f'{project_data.API_BDY_1}{url}{project_data.API_BDY_2}')

print(query)
put_log = query.content.decode('utf-8')

with open('log/put_log.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(put_log, f, indent=4)

"""
data_put = query.content.decode(encoding='utf-8')

with open('log/tmp.xml', mode='w', encoding='utf-8') as f:
    f.write(data_put)

tmp = etree.parse('log/tmp.xml')
xml_put = etree.tostring(tmp, pretty_print = True, encoding = str)

with open('log/put.xml', mode='w') as f:
    f.write(xml_put)

os.remove('log/tmp.xml')
"""