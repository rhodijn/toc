#!/usr/bin/env python3

import json, project_data, requests

mms_id = 991030022319705501

get_url = f'{project_data.API_URL}{mms_id}?view={project_data.API_VIEW}&expand={project_data.API_EXP} \
    &apikey={project_data.API_KEY}&format={project_data.API_FRMT}'

query = requests.get(get_url)

data = json.loads(query.content.decode(encoding='utf-8'))

with open('log/get.json', mode='w', encoding='utf-8') as f:
    f.seek(0)
    json.dump(data, f, indent=4)

put_url = f'{project_data.API_URL}{mms_id}?validate=true&override_warning=true&override_lock=true&stale_version_check=false&cataloger_level=20&check_match=false&apikey={project_data.API_KEY}'

response = requests.put(put_url, data=project_data.API_BDY)

with open('log/put.txt', mode='w') as f:
    f.write(str(response))

# print(response.decode('utf-8'))