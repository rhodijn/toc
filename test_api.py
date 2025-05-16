#!/usr/bin/env python3

import project_data, requests

mms_id = 991030022319705501

alma_query = requests.get(f'{project_data.API_URL}{mms_id}?view={project_data.API_VIEW}&expand={project_data.API_EXP}&apikey={project_data.API_KEY}')

print(alma_query.content)