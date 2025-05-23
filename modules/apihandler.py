#!/usr/bin/env python3
#
#   ##################      this module communicates with alma
#   ##                ##    version 0.1, 2025-05-23
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import argparse, os, re
from dotenv import dotenv_values


secrets = dotenv_values('.env')