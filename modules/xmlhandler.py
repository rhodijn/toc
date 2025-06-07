#!/usr/bin/env python3
#
#   ###################      this module handles xml data
#   ##                 ##    version 0.7 (2025-06-06)
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##    created by rhodijn (zolo) for zhaw hsb
#   ##                 ##
#     ###################    licensed under the apache license, version 2.0
#
#===============================================================================


import os

from dotenv import dotenv_values
from lxml import etree


secrets = dotenv_values('.env')
xml_declaration = '<?xml version="1.0" encoding="UTF-8" ?>\n'


def save_to_xml(processing: dict, data_xml: dict) -> dict:
    """
    convert json to xml

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = 
    param_1: str = 
    param_2: str =
    """
    try:
        with open('temp/temp.xml', mode='w', encoding='utf-8') as f:
            f.write(data_xml)

        tmp = etree.parse('temp/temp.xml')
        data_xml = etree.tostring(tmp, pretty_print=True, encoding=str)

        with open(f"temp/{processing['mms_id']['iz']}.xml", mode='w', encoding='utf-8') as f:
            f.write(data_xml)

        # os.remove('temp/temp.xml')
        # os.remove(f"temp/{data_json['mms_id']}.json")

        processing.update({'xml_saved': True})
        processing['messages'].append('record saved as xml')
    except:
        processing['messages'].append('saving xml-file failed')

    return processing


def add_856_field(processing: dict) -> dict:
    """
    adds a field 856 to the record with the correct url

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = 
    param_1: str = 
    param_2: str =
    """
    field_856 = etree.parse('data/856.xml')
    root_856 = field_856.getroot()

    try:
        tree = etree.parse(f"temp/{processing['mms_id']['iz']}.xml")
        root = tree.getroot()
        root_856.find("./subfield[@code='u']").text = processing['url']
        root.find('./record').append(root_856)

        data_xml = etree.tostring(root, pretty_print=True, encoding=str)
        with open(f"xml/{processing['mms_id']['iz']}.xml", mode='w', encoding='utf-8') as f:
            f.write(xml_declaration + data_xml)

        # os.remove(f"temp/{processing['mms_id']['iz']}.xml")

        processing.update({'added_856': True})
        processing['messages'].append('added field 856')
    except:
        processing['messages'].append('failed to add field 856')

    return processing