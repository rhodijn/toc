#!/usr/bin/env python3

##################      this is the main routine
##                ##    version 0.1, 2025-05-23
##              ##
  ######      ##        python main.py -f toc/local/BM2064158.pdf -l win
    ##      ######
  ##              ##    created by rhodijn for zhaw hsb
##                ##
  ##################    cc-by-sa [°_°]


import sys
sys.path.append('modules/')

from apihandler import *
from checker import *
from logger import *
from uploader import *


if __name__ == '__main__':
    """
    this is the __main__ routine, it controls the process
    """
    args = get_args()
    valid_file, msg = check_file(args.file)
    if valid_file:
        barcode = args.file.split('/')[-1].split('.')[0]
        valid_lib, msg = check_lib(args.lib.lower())
        if valid_lib:
            print(msg)
        else:
            print(msg)