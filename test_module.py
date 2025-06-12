#!/usr/bin/env python3
#
#   ###################      this is the main routine
#   ##                 ##    version 1.0 (2025-06-10)
#   ##               ##
#     ######       ##        python enrich.py -f toc/local/BM2064158.pdf -l win
#       ##       ######
#     ##               ##    created by rhodijn (zolo) for zhaw hsb
#   ##                 ##
#     ###################    licensed under the apache license, version 2.0
#
#===============================================================================


import argparse, datetime, dotenv, email, json, lxml, os, paramiko, requests, re, smtplib, ssl, sys

print('all modules imported')