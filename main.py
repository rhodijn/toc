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

import json, os, requests
from dotenv import load_dotenv
from filechecker import *

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
        print(args.file.split('/')[-1].split('.')[0])