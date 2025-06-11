#!/usr/bin/env python3
#
#   ###################      this module handles xml data
#   ##                 ##    version 1.0 (2025-06-10)
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


def save_to_xml(processing: dict, data_xml: dict) -> dict:
    """
    convert data to xml-file

    parameters:
    processing: dict = logging info of the currently processed record
    data_xml: dict = data to save to xml-file

    returns:
    processing: dict = logging info of the currently processed record
    """
    try:
        with open(f"temp/{processing['mms_id']['iz']}.xml", mode='w', encoding='utf-8') as f:
            f.write(data_xml)

        processing.update({'xml_saved': True})
        processing['messages'].append('record saved as xml')
    except:
        processing['messages'].append('saving xml-file failed')

    return processing


def add_856_field(processing: dict) -> dict:
    """
    adds a field 856 to the record with the correct url

    parameters:
    processing: dict = logging info of the currently processed record

    returns:
    processing: dict = logging info of the currently processed record
    """
    XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8" ?>\n'

    field_856 = etree.parse('data/856.xml')
    root_856 = field_856.getroot()

    try:
        tree = etree.parse(f"temp/{processing['mms_id']['iz']}.xml")
        root = tree.getroot()
        root_856.find("./subfield[@code='u']").text = processing['url']
        root.find('./record').append(root_856)

        data_xml = etree.tostring(root, pretty_print=True, encoding=str)
        with open(f"xml/{processing['mms_id']['iz']}.xml", mode='w', encoding='utf-8') as f:
            f.write(XML_DECLARATION + data_xml)

        os.remove(f"temp/{processing['mms_id']['iz']}.xml")

        processing.update({'added_856': True})
        processing['messages'].append('field 856 added')
    except:
        processing['messages'].append('failed to add field 856')

    return processing