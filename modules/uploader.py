#!/usr/bin/env python3
#
#   ##################      this module handles the upload
#   ##                ##    version 0.1, 2025-05-23
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import os, paramiko

from dotenv import load_dotenv


load_dotenv()

ftp_url = os.getenv('FTP_URL')
ftp_user = os.getenv('FTP_USER')
ftp_pass = os.getenv('FTP_PASS')