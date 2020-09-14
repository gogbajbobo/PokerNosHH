# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import requests
import credentials
import json
from os import path

# %%
url = f'{credentials.host}{":" + credentials.port if credentials.port else ""}{credentials.location}'
payload = {'Password': credentials.api_pass, 'Command': 'LogsHandHistory', 'JSON': 'Yes'}
response = requests.get(url, payload)
data = response.json()
number_of_files = data["Files"]
print(f'Files: {number_of_files}')
print(data['Date'])

# %%
hh_data_dirname = 'hh_data'

for i in range(number_of_files):
    date = data['Date'][i]
    name = data['Name'][i]
    payload['Date'] = date
    payload['Name'] = name
    print(f'get {date} - {name} hand history')
    response = requests.get(url, payload)
    print(f'got {len(response.content)} bytes')
    filename = path.join(hh_data_dirname, f'{date}-{name}.txt')
    with open(filename, 'w') as file:
        json.dump(response.json(), file)
        print(f'save hand history to {filename}')

# %%
