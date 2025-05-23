#!/usr/bin/env python3
#
#   ##################      this module communicates with alma
#   ##                ##    version 0.2 (2025-05-23)
#   ##              ##
#     ######      ##
#       ##      ######
#     ##              ##    created by rhodijn (zolo) for zhaw hsb
#   ##                ##
#     ##################    cc-by-sa [°_°]


import requests

from dotenv import dotenv_values
from logger import *


secrets = dotenv_values('.env')


def get_request(code) -> requests.models.Response:
    """
    write json file

    parameters:
    d: dict = data to be logged
    filename: str = library code
    p: str = code for path

    returns:
    response: requests.models.Response = success saving data
    """

    config = json_load('config.json', 'd')
    response = requests.get(f'{config["api"]["url"]}items?item_barcode={code}&apikey={secrets["API_KEY"]}&format={config["api"]["j"]}')
    return response