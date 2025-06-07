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


url = 'https://slspmedia.hsb.zhaw.ch/public/swisscovery/inhaltsverzeichnis/winterthur/991017945329705501.pdf'
field_856 = etree.parse('data/856.xml')
r = field_856.getroot()

file_list = os.listdir('temp/')


for f in file_list:
    attrib_l = []
    attrib_l_a = []
    attrib_l_num = []

    tree = etree.parse(f"temp/{f}")
    root = tree.getroot()

    for child in root:
        if child.tag == 'datafield':
            attrib_l.append(child.attrib['tag'])
            if child.attrib['tag'] == '856':
                print(f"{child.attrib['tag']}:")
                for ancestor in child:
                    print(f"\t${ancestor.attrib['code']}: {ancestor.text}")

    r.find("./subfield[@code='u']").text = url
    root.append(r)

    """
    if '856' in attrib_l:
        print(attrib_l.index('856'))
        root.insert(attrib_l.index('856') + 1, r)
    """

    attrib_l_a = sorted([el for el in attrib_l if not el.isnumeric()])
    attrib_l_num = sorted([int(el) for el in attrib_l if el.isnumeric()])

    attrib_list = attrib_l_num + attrib_l_a
    print(attrib_list)

    data_xml = etree.tostring(root, pretty_print=True, encoding=str)
    with open(f"temp/t_{f}", mode='w', encoding='utf-8') as f:
        f.write(data_xml)