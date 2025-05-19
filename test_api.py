#!/usr/bin/env python3

import json, project_data, requests

mms_id = 991030022319705501

query = requests.get(f'{project_data.API_URL}{mms_id}?view={project_data.API_VIEW}&expand={project_data.API_EXP} \
                     &apikey={project_data.API_KEY}&format={project_data.API_FRMT}')

data = json.loads(query.content.decode(encoding='utf-8'))

with open('log/query.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(data, f, indent=4)