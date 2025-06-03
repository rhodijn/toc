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


file_list = os.listdir('temp/')
attrib_list = []

for f in file_list:
    tree = etree.parse(f"temp/{f}")
    root = tree.getroot()

    for child in root:
        if child.tag == 'datafield':
            print(child)
            attrib_list.append(child.attrib['tag'])
            if child.attrib['tag'] == '856':
                print(f"{child.attrib['tag']}:")
                for ancestor in child:
                    print(f"\t${ancestor.attrib['code']}: {ancestor.text}")

    if '856' in attrib_list:
        print('ja')
        print(attrib_list.index('856'))

    field_856 = {'ind1': '4', 'ind2': '2', 'tag': '856'}

    tree.write(f"temp/{f}")