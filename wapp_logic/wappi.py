import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from configs import config


def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class Wappi:

    def __init__(self, wapp_data):
        self.profile_id = wapp_data['instanceId']
        self.url = 'https://wappi.pro/'
        self.token = config.wappi_key
        self.headers = {
            'Authorization': self.token
        }

    def set_settings(self, state=False):
        if state:
            return Wappi_instance().set_webhook_settings(self.profile_id, state_webhook=False)
        else:
            return Wappi_instance().set_webhook_url(self.profile_id)


class Wappi_instance:

    def __init__(self):
        self.token = config.wappi_key
        self.url = self.url = 'https://wappi.pro/'
        self.headers = {
            'Authorization': self.token
        }

    def set_webhook_url(self, profile_id, webhook_url='https://www.botsarmy.biz/beauty_wapp'):
        url = self.url + 'api/webhook/url/set'
        params = {
            'profile_id': profile_id,
            'url': webhook_url
        }
        r = requests.post(url, headers=self.headers, params=params)
        try:

            return r.json().get('result')
        except:
            return r.text

    def set_webhook_settings(self, profile_id, state_webhook=False):
        url = self.url + 'api/webhook/types/set'
        params = {
            'profile_id': profile_id
        }
        data = ['incoming_message', 'outgoing_message_api', 'outgoing_message_phone']
        if state_webhook:
            data.append('authorization_status')
        r = requests.post(url, headers=self.headers, params=params, json=data)
        try:
            return r.json().get('result')
        except:
            return r.text
