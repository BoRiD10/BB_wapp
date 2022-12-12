import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class Bot:

    def __init__(self, token):
        self.token = token
        self.url = 'https://api.telegram.org/bot{!s}/'.format(self.token)

    def send_message(self, user_id, text, reply_markup={}, markdown='Markdown', disable_web_page_preview=True,
                     disable_notification=False, session=None):
        url = self.url + 'sendMessage'

        if 'jpeg' in text or 'png' in text or 'jpg' in text or 'oga' in text:
            disable_web_page_preview = False

        params = {
            'chat_id': user_id,
            'text': text,
            'parse_mode': markdown,
            'reply_markup': reply_markup,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification
        }

        if session is None:
            r = get_session().post(url, json=params)
        else:
            r = session.post(url, json=params)

        assert r.status_code in [200, 403, 400, 429], '{}\n\n{}'.format(r.text, params)

        return r


