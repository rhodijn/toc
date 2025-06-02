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

    returns:
    response: tuple = request: str, response: requests.models.Response
    """
    with open('temp/temp.xml', mode='w', encoding='utf-8') as f:
        f.write(data_json['anies'][0])

    tmp = etree.parse('temp/temp.xml')
    data_xml = etree.tostring(tmp, pretty_print=True, encoding=str)

    with open(f"temp/{data_json['mms_id']}.xml", mode='w', encoding='utf-8') as f:
        f.write(data_xml)