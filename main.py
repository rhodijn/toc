#!/usr/bin/env python3

##################      this is the main routine
##                ##    version 0.1, 2025-05-23
##              ##
  ######      ##        python3 main.py -f toc/BM2064158.pdf -l win
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
        print(args.file.split('/')[-1].split('.')[0])