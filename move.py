#!/usr/bin/env python3

import ftplib, os, project_data, re

file_list = sorted(os.listdir(project_data.TOC_PATH))

for f in file_list:
    if not re.search('^\\d+.pdf', f):
        file_list.remove(f)

print(file_list)