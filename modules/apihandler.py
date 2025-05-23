#!/usr/bin/env python3

##################      this module communicates with alma
##                ##    version 0.1, 2025-05-23
##              ##
  ######      ##
    ##      ######
  ##              ##    created by rhodijn for zhaw hsb
##                ##
  ##################    cc-by-sa [°_°]


import argparse, os, re
from dotenv import load_dotenv


load_dotenv()

api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')