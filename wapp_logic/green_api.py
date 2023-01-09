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


class Green_Api:

    def __init__(self, wapp_data):

        self.instance_id = wapp_data['instanceId']
        self.url = 'https://api.green-api.com/waInstance{}'.format(self.instance_id)
        self.token = wapp_data['token']

    def set_settings(self, webhook_url='https://www.botsarmy.biz/beauty_wapp', state=False):
        url = self.url + '/SetSettings/{}'.format(self.token)
        params = {
            "webhookUrl": webhook_url,
            "delaySendMessagesMilliseconds": 500,
            "outgoingWebhook": "no",
            "outgoingMessageWebhook": "yes",
            "incomingWebhook": "yes",
            "outgoingAPIMessageWebhook": "yes",
            "enableMessagesHistory": "yes",
            'stateWebhook': 'yes'
        }
        if state:
            params['stateWebhook'] = 'no'
        r = requests.post(url=url, json=params)
        return r.json()
