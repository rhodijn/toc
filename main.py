#!/usr/bin/env python3


################      this is the main script for the toc project
##              ##
##            ##
  ######    ##        version 0.1, 2025-05-23
    ##    ######
  ##            ##
##              ##
  ################    created by rhodijn for zhaw hsb, cc-by-sa [°_°]


import sys
sys.path.append('modules/')

from dotenv import load_dotenv
from file_checker import *
import json, os, requests

load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
ftp_url = os.getenv('FTP_URL')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')

if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    args = get_args()
    valid_file = check_file(args.file)
    if valid_file:
        barcode = get_barcode(args.file)
        print(barcode)