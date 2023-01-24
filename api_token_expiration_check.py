import os
from util.common import get_server_info, call_hdx_endpoint, call_to_hdx_with_recorded_time

ACTION_NAME = 'notify_users_about_api_token_expiration'
FILENAME = 'times_token_expiration.csv'


def start_process(url: str, is_prod: bool):
    token = os.environ.get('HDX_API_TOKEN')
    data_7_days = {
        'days_in_advance': 7,
        'expires_on_specified_day': True
    }
    data_2_days = {
        'days_in_advance': 2,
        'expires_on_specified_day': False
    }
    headers = {
        'Authorization': token,
        'User-Agent': 'HDXINTERNAL_STATS_TRIGGER',
        'content-type': 'application/json'
    }
    call_to_hdx_with_recorded_time(url, headers, data_7_days, FILENAME, f'7 days check - URL {url}')
    call_to_hdx_with_recorded_time(url, headers, data_2_days, FILENAME, f'2 days check - URL {url}')


if __name__ == '__main__':
    base_url, is_prod = get_server_info()
    start_process(base_url + ACTION_NAME, is_prod)
