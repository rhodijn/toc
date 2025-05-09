#!/usr/bin/env python3

import datetime, pprint

f_process = {}

f_name = '123.pdf'

f_process.update(
    {
        f_name: {
            'dt': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'filename': f_name,
            'valid': False,
            'upload': False,
            'deleted': False,
            'messages': [],
            'url': None, 
            'mms-id': None
        }
    }
)

pprint.pp(f_process)

f_process[f_name]['messages'].append('file not pdf format')

pprint.pp(f_process[f_name]['messages'])

f_process[f_name]['messages'].append('file not found')

pprint.pp(f_process[f_name]['messages'])