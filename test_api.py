#!/usr/bin/env python3

import project_data, requests
import xml.etree.ElementTree as ET

mms_id = 991030022319705501

alma_query = requests.get(f'{project_data.API_URL}{mms_id}?view={project_data.API_VIEW}&expand={project_data.API_EXP}&apikey={project_data.API_KEY}')

with open('test.xml', 'wb') as f:
    f.write(alma_query.content)

tree = ET.parse('test.xml')
root = tree.getroot()

for item in root.findall('./'):
    for child in item:
        print(f'{item.tag}: {child.tag}')