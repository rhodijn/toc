#!/usr/bin/env python3


################      this is the main script for the toc project
##              ##
##            ##
  ######    ##        version 0.1, 2025-05-23
    ##    ######
  ##            ##
##              ##
  ################    created by rhodijn for zhaw hsb, cc-by-sa [°_°]


import argparse, os, re


def get_args() -> argparse.Namespace:
    """
    get path to toc file from input

    returns:
    args.file: argparse.Namespace = path to to file
    """
    parser = argparse.ArgumentParser(
        prog = 'toc uploader',
        description = 'upload toc to ftp-server from terminal',
        epilog = 'zhaw hsb, cc-by-sa'
    )

    parser.add_argument('-f', '--file', required=True, type=str, help='path to toc-file (including name)')
    parser.add_argument('-l', '--lib', required=True, type=str, help='library, used for remote path')

    args = parser.parse_args()

    return args


def check_file(path):
    if os.path.exists(path):
        if re.search('(pdf|PDF)', path.split('/')[-1].split('.')[-1]):
            return True
    else:
        return False


def get_barcode(path):
    elements = path.split('/')
    barcode = elements[-1].split('.')[0]
    return barcode
