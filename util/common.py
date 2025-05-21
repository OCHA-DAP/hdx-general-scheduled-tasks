import csv
import datetime
import json
import os
import sys

import requests

FOLDER_NAME = 'data'
MAIN_URL = 'https://data.humdata.org/api/3/action/'
DEV_URL = 'https://{}.data-humdata-org.ahconu.org/api/3/action/'


def get_server_info() -> (str, bool):
    is_prod = False
    url = DEV_URL.format('dev')
    if len(sys.argv) == 2:
        server = sys.argv[1]
        if server == 'main':
            url = MAIN_URL
            is_prod = True
        elif server in ['dev', 'feature', 'stage', 'demo']:
            url = DEV_URL.format(server)
    return url, is_prod


def call_hdx_endpoint(url: str, headers: dict, data:  dict, verify=True) -> dict:
    r = requests.post(url, data=json.dumps(data), headers=headers, verify=verify)
    r.raise_for_status()
    try:
        return r.json()
    except Exception as e:
        print(f"Error parsing JSON response: status_code={r.status_code}, content={r.text}")
        raise
    

def create_folder_if_necessary(folder_name):
    os.makedirs(os.path.dirname(folder_name), exist_ok=True)


def create_file_if_necessary(filename_path):
    if not os.path.isfile(filename_path):
        with open(filename_path, 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(['TIMESTAMP', 'DURATION IN MS', 'DESCRIPTION'])
        print('CSV file created')


def add_duration_to_file(duration: int, description: str, filename: str):
    create_folder_if_necessary('{}/'.format(FOLDER_NAME))
    filename_path = '{}/{}'.format(FOLDER_NAME, filename)
    create_file_if_necessary(filename_path)

    with open(filename_path, 'a', newline='') as out:
        writer = csv.writer(out)
        now = datetime.datetime.utcnow().isoformat()
        writer.writerow([now, duration, description])


def call_to_hdx_with_recorded_time(url: str, headers: dict, data: dict, filename: str, description=''):
    start_time = datetime.datetime.utcnow()
    call_hdx_endpoint(url, headers, data)
    end_time = datetime.datetime.utcnow()
    duration_in_ms = round((end_time - start_time).total_seconds() * 1000)
    add_duration_to_file(duration_in_ms, description, filename)
