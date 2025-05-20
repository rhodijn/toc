#!/usr/bin/env python3

from lxml import etree
import project_data, os, requests

mms_id = 9947393580105520
url = 'https://slspmedia.hsb.zhaw.ch/public/swisscovery/inhaltsverzeichnis/winterthur/995860000000545473.pdf'

get_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_GET}&apikey={project_data.API_KEY}&format={project_data.API_FRMT}'

query = requests.get(get_url)

data = query.content.decode(encoding='utf-8')

with open('log/tmp.xml', mode='w', encoding='utf-8') as f:
    f.write(data)

put_url = f'{project_data.API_URL}{mms_id}{project_data.API_PARA_PUT}&apikey={project_data.API_KEY}'

response = requests.put(put_url, headers=project_data.API_HDR, data=f'{project_data.API_BDY_1}{url}{project_data.API_BDY_2}')

with open('log/put.xml', mode='w') as f:
    f.write(str(response))

tmp = etree.parse('log/tmp.xml')
new_xml = etree.tostring(tmp, pretty_print = True, encoding = str)

with open('log/get.xml', mode='w') as f:
    f.write(new_xml)

os.remove('log/tmp.xml')