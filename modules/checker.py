#!/usr/bin/env python3
#
#   ##################      this module checks the file
#   ##                ##    version 0.7 (2025-05-26)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]
#
#===============================================================================


import argparse, json, os, re


def get_args() -> argparse.Namespace:
    """
    get arguments submitted with command line tool

    returns:
    args.file: argparse.Namespace = clt arguments
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


def check_file(path: str) -> tuple:
    """
    check if file parameter exists and is pdf

    parameters:
    path: str = path to toc-file

    returns:
    tuple
    """
    if os.path.exists(path):

        if re.search('(pdf|PDF)', path.split('/')[-1].split('.')[-1]):
            return True, 'local file valid'
        else:
            return False, 'local file invalid format'
    else:
        return False, 'local file does not exist'


def check_lib(lib: str) -> tuple:
    """
    check if library parameter is valid

    parameters:
    lib: str = library code

    returns:
    tuple
    """
    try:
        with open('data/config.json') as f:
            data = json.load(f)

            if lib in data['library'].keys():
                return True, 'library code valid'
            else:
                return False, 'library code invalid'
    except Exception as e:
        return False, f"error: {e}"