#!/usr/bin/env python3
#
#   ###################      this script is for testing the alma api
#   ##                 ##    version 0.4 (2025-06-03)
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
import os


field_856 = etree.parse('data/856.xml')
r = field_856.getroot()

file_list = os.listdir('temp/')

for f in file_list:
    attrib_list = []

    tree = etree.parse(f"temp/{f}")
    root = tree.getroot()

    for child in root:
        if child.tag == 'datafield':
            attrib_list.append(child.attrib['tag'])
            if child.attrib['tag'] == '856':
                print(f"{child.attrib['tag']}:")
                for ancestor in child:
                    print(f"\t${ancestor.attrib['code']}: {ancestor.text}")
        root.append(r)

    if '856' in attrib_list:
        print('ja')
        print(attrib_list.index('856'))
        root.insert(attrib_list.index('856') + 1, r)

    data_xml = etree.tostring(root, pretty_print=True, encoding=str)
    with open(f"temp/t_{f}", mode='w', encoding='utf-8') as f:
        f.write(data_xml)

    """
    tree = etree.parse(f"temp/t_{f}")
    root = tree.getroot()

    data_xml = etree.tostring(root, pretty_print=True, encoding=str)
    with open(f"temp/d_{f}", mode='w', encoding='utf-8') as f:
        f.write(data_xml)
    """