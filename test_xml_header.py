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


XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8" ?>\n'
tree = etree.parse('temp/note.xml')
root = tree.getroot()


data_xml = etree.tostring(root, pretty_print=True, encoding=str)
with open(f"temp/note_2.xml", mode='w', encoding='utf-8') as f:
    f.write(XML_DECLARATION + data_xml)