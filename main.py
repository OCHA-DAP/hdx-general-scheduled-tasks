import csv

import os

import requests

FOLDER_NAME = 'data'
URL = 'https://dev.data-humdata-org.ahconu.org/api/3/action/hdx_push_general_stats'
# URL = 'https://data.humdata.local/api/3/action/hdx_push_general_stats'

CSV_HEADERS = [
        'DATASETS TOTAL',
        'DATASETS IN QA',
        'DATASETS QA COMPLETED',
        'DATASETS WITH QUARANTINE',
        'DATASETS WITH NO QUARANTINE',
        'ORGS TOTAL',
        'ORGS WITH DATASETS',
        'ORGS UPDATING DATA IN PAST YEAR',
    ]


def start_process():
    create_folder_if_necessary('{}/'.format(FOLDER_NAME))
    filename = '{}/results.csv'.format(FOLDER_NAME)
    create_file_if_necessary(filename)

    result = call_hdx_endpoint()

    if result['success']:
        with open(filename, 'a', newline='') as out:
            stats = result['result']['mixpanel_meta']
            writer = csv.writer(out)
            data = [
                stats.get('datasets total'),
                stats.get('datasets in qa'),
                stats.get('datasets qa completed'),
                stats.get('datasets with quarantine'),
                stats.get('datasets with no quarantine'),
                stats.get('orgs total'),
                stats.get('orgs with datasets'),
                stats.get('orgs updating data in past year'),
            ]
            writer.writerow(data)
            print('Finished adding row')


def create_folder_if_necessary(folder_name):
    os.makedirs(os.path.dirname(folder_name), exist_ok=True)


def create_file_if_necessary(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(CSV_HEADERS)
        print('CSV file created')


def call_hdx_endpoint():
    token = os.environ.get('HDX_API_TOKEN')
    headers = {
        'Authorization': token,
        'User-Agent': 'HDXINTERNAL_STATS_TRIGGER',
        'content-type': 'application/json'
    }
    r = requests.post(URL, data={}, headers=headers, verify=False)
    r.raise_for_status()
    return r.json()


# class NoDataException(Exception):
#     def __init__(self, message, errors=None):
#         super().__init__(message)
#         self.errors = errors


if __name__ == '__main__':
    start_process()
