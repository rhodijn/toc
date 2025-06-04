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


def quicksort(x):
    if len(x) <= 1:
        return x
    else:
        pivot = x[0]
        i = 0
        for j in range(len(x) - 1):
            if x[j + 1] < pivot:
                x[j + 1], x[i + 1] = x[i + 1], x[j + 1]
                i += 1
        x[0], x[i] = x[i], x[0]
        first_part = quicksort(x[:i])
        second_part = quicksort(x[i + 1:])
        first_part.append(x[i])
        return first_part + second_part


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
        root.append(r)

    if '856' in attrib_l:
        print(attrib_l.index('856'))
        root.insert(attrib_l.index('856') + 1, r)

    for el in attrib_l:
        if not el.isnumeric():
            attrib_l_a.append(el)

        attrib_l_num = [int(el) for el in attrib_l if el.isnumeric()]

        print(attrib_l_num)
        attrib_l_sorted = quicksort(attrib_l_num)
        print(attrib_l_sorted)
        print(attrib_l_a)

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