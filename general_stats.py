import os

from util.common import get_server_info, call_to_hdx_with_recorded_time

# URL = 'https://data.humdata.local/api/3/action/hdx_push_general_stats'

ACTION_NAME = 'hdx_push_general_stats'
FILENAME = 'times_general_stats.csv'

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


def start_process(url: str, is_prod: bool):
    token = os.environ.get('HDX_API_TOKEN')
    headers = {
        'Authorization': token,
        'User-Agent': 'HDXINTERNAL_STATS_TRIGGER',
        'content-type': 'application/json'
    }
    call_to_hdx_with_recorded_time(url, headers, {}, FILENAME, f'URL: {url}')

    # if result['success']:
    #     with open(filename, 'a', newline='') as out:
    #         stats = result['result']['mixpanel_meta']
    #         writer = csv.writer(out)
    #         data = [
    #             stats.get('datasets total'),
    #             stats.get('datasets in qa'),
    #             stats.get('datasets qa completed'),
    #             stats.get('datasets with quarantine'),
    #             stats.get('datasets with no quarantine'),
    #             stats.get('orgs total'),
    #             stats.get('orgs with datasets'),
    #             stats.get('orgs updating data in past year'),
    #         ]
    #         writer.writerow(data)
    #         print('Finished adding row')


# def create_file_if_necessary(filename):
#     if not os.path.isfile(filename):
#         with open(filename, 'w', newline='') as out:
#             writer = csv.writer(out)
#             writer.writerow(CSV_HEADERS)
#         print('CSV file created')


# class NoDataException(Exception):
#     def __init__(self, message, errors=None):
#         super().__init__(message)
#         self.errors = errors


if __name__ == '__main__':
    base_url, is_prod = get_server_info()
    start_process(base_url + ACTION_NAME, is_prod)
