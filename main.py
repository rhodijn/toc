#!/usr/bin/env python3
#
#   ##################      this is the main routine
#   ##                ##    version 0.1, 2025-05-23
#   ##              ##
#     ######      ##        python main.py -f toc/local/BM2064158.pdf -l win
#       ##      ######
#     ##              ##    created by rhodijn for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import sys
sys.path.append('modules/')

from apihandler import *
from checker import *
from logger import *
from uploader import *

import datetime


processing = {}
log = {}

if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    log = json_ld(f'log_{datetime.datetime.now().strftime("%Y")}.json', 'l')
    args = get_args()
    barcode = args.file.split('/')[-1].split('.')[0].upper()

    if barcode not in log.keys():
        processing = json_ld('log.json', 'd')
        processing.update({'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        processing['filename'].update({'local': args.file.split('/')[-1]})
    else:
        processing = log[barcode]

    valid_file, msg = check_file(args.file)
    processing['messages'].append(msg)

    if valid_file:
        processing['valid'].update({'file': True})
        valid_lib, msg = check_lib(args.lib.lower())
        processing['messages'].append(msg)

        if valid_lib:
            processing['valid'].update({'lib': True})

    log.update({barcode: processing})

    json_wr(log, f'log_{datetime.datetime.now().strftime("%Y")}.json', 'l')