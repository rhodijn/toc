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


def json_to_xml(processing: dict, data_json: dict) -> dict:
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
            f.write(data_json['anies'][0])

        tmp = etree.parse('temp/temp.xml')
        data_xml = etree.tostring(tmp, pretty_print=True, encoding=str)

        with open(f"temp/{data_json['mms_id']}.xml", mode='w', encoding='utf-8') as f:
            f.write(data_xml)

        # os.remove('temp/temp.xml')
        # os.remove(f"temp/{data_json['mms_id']}.json")

        processing.update({'xml_saved': True})
        processing['messages'].append('record saved as xml')
    except:
        processing['messages'].append('saving xml-file failed')

    return processing


def add_856_field(processing: dict, data_json: dict) -> dict:
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
        tree = etree.parse(f"temp/{data_json['mms_id']}.xml")
        root = tree.getroot()
        root_856.find("./subfield[@code='u']").text = processing['url']
        root.append(root_856)

        data_xml = etree.tostring(root, pretty_print=True, encoding=str)
        with open(f"xml/{data_json['mms_id']}.xml", mode='w', encoding='utf-8') as f:
            f.write(data_xml)

        # os.remove(f"temp/{data_json['mms_id']}.xml")

        processing.update({'added_856': True})
        processing['messages'].append('added field 856')
    except:
        processing['messages'].append('failed to add field 856')

    return processing