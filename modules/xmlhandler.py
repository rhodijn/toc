#!/usr/bin/env python3
#
#   ###################      this module handles xml data
#   ##                 ##    version 0.1 (2025-06-02)
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


def json_to_xml(data_json: dict):
    """
    convert json to xml

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = 
    param_1: str = 
    param_2: str =
    """
    with open('xml/temp/temp.xml', mode='w', encoding='utf-8') as f:
        f.write(data_json['anies'][0])

    tmp = etree.parse('xml/temp/temp.xml')
    data_xml = etree.tostring(tmp, pretty_print=True, encoding=str)

    with open(f"xml/{data_json['mms_id']}.xml", mode='w', encoding='utf-8') as f:
        f.write(data_xml)
    
    os.remove('xml/temp/temp.xml')
    os.remove(f"xml/temp/{data_json['mms_id']}.json")


def add_856_field(processing: dict) -> dict:
    """
    adds a field 856 to the record with the correct url

    parameters:
    method: str = api request method (GET, PUT, POST, ...)
    value: str = 
    param_1: str = 
    param_2: str =
    """