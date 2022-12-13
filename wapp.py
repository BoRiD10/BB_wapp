import base64
from datetime import datetime

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import mongo
from configs import config
from telegram import Bot


def wapp_info(text):
    logger.remove()
    logger.add('BB_wapp/logs/wapp/wapp_info.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class GreenApi:

    def __init__(self, name, wapp_data):
        self.name = name
        self.instanceId = wapp_data['instanceId']
        self.url = 'https://api.green-api.com/waInstance{}'.format(self.instanceId)
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
            "enableMessagesHistory": "yes"
        }
        if state:
            params = {
                'stateWebhook': 'no'
            }
        r = requests.post(url=url, json=params)
        return r.json()

    def get_settings(self):
        """ Получает настройки аккаунта """

        url = self.url + '/GetSettings/{}'.format(self.token)
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.get(url=url, headers=headers)
        try:
            return r.json()
        except:
            return r.text

    def get_status(self):
        url = self.url + '/GetStateInstance/{}'.format(self.token)

        r = requests.get(url=url)
        if r.status_code == 400:
            return {'error': 'no response'}
        else:
            r = r.json()

        if 'stateInstance' in r:
            if r['stateInstance'] == 'notAuthorized':
                return {'accountStatus': 'got qr code'}
            elif r['stateInstance'] == 'sleepMode':
                return {'accountStatus': 'loading', 'statusData': {'title': 'не подключен'}}
            elif r['stateInstance'] == 'authorized':
                return {'accountStatus': 'authenticated', 'statusData': {'title': 'подключен ok'}}
            if r['stateInstance'] == 'blocked':
                return {'accountStatus': 'blocked', 'statusData': {'title': 'Заблокирован'}}
        else:
            return {'error': 'no response'}

    def reboot(self):
        url = self.url + '/Reboot/{}'.format(self.token)
        r = requests.get(url=url).json()
        if r['isReboot']:
            data = {'success': True}
        else:
            data = {'success': False}
        return data

    def logout(self):
        url = self.url + '/Logout/{}'.format(self.token)
        return requests.get(url=url).json()

    def get_qr(self):
        """Возвращает объект image в bytes, готовый для отправки в бота тг методом send_bytes_Photo"""
        url = 'https://api.green-api.com/waInstance{}/qr/{}'.format(self.instanceId, self.token)
        r = get_session().get(url=url)
        try:
            file = base64.b64decode(r.json()['message'])
        except:
            if type(r) is str:
                return r
            return r.json()['message']

        return file

    def get_clean_qr(self):
        """Возвращает объект image в bytes, готовый для отправки в бота тг методом send_bytes_Photo"""
        url = 'https://api.green-api.com/waInstance{}/qr/{}'.format(self.instanceId, self.token)
        r = get_session().get(url=url)
        return r.json()

    def send_message(self, chatId, message):
        url = self.url + '/SendMessage/{}'.format(self.token)

        if '-' in chatId:
            send_to = chatId + '@g.us'
        else:
            send_to = chatId + '@c.us'

        params = {
            'chatId': send_to,
            'message': message
        }
        r = requests.post(url=url, json=params)
        return r.json()

    def send_location(self, chat_id, latitude, longitude, address=None):
        url = self.url + '/SendLocation/{}'.format(self.token)
        if '-' in chat_id:
            send_to = chat_id + '@g.us'
        else:
            send_to = chat_id + '@c.us'

        params = {
            'chatId': send_to,
            'latitude': latitude,
            'longitude': longitude
        }

        if address is not None:
            params['address'] = address

        return requests.post(url=url, json=params).json()

    def check_exist(self, phone):
        url = self.url + '/CheckWhatsapp/{}'.format(self.token)
        params = {
            'phoneNumber': int(phone)
        }

        return requests.post(url=url, json=params, timeout=1).json()

    def send_file(self, chat_id, url_file, caption=None):
        url = self.url + '/SendFileByUrl/{}'.format(self.token)
        headers = {
            'Content-Type': 'application/json'
        }

        if '-' in chat_id:
            chat_id = chat_id + '@g.us'
        else:
            chat_id = chat_id + '@c.us'

        params = {
            'chatId': chat_id,
            'urlFile': url_file,
            'fileName': url_file.split('/')[-1],
        }

        if caption is not None:
            params['caption'] = caption

        return requests.post(url=url, json=params, headers=headers).json()

    def send_contact(self, chat_id, phone, name):
        url = self.url + '/sendContact/{}'.format(self.token)
        headers = {
            'Content-Type': 'application/json'
        }

        if '-' in chat_id:
            chat_id = chat_id + '@g.us'
        else:
            chat_id = chat_id + '@c.us'

        params = {
            'chatId': chat_id,
            'contact': {
                'phoneContact': phone,
                'firstName': name
            }
        }

        return requests.post(url=url, json=params, headers=headers).json()

    def message_q(self):
        url = self.url + '/ShowMessagesQueue/{}'.format(self.token)

        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.get(url=url, headers=headers).json()
        if len(r) == 0:
            return {'totalMessages': 0, 'first100': []}
        else:
            first100 = [{'last_try': 'N/A', 'body': msg.get('message', ''), 'chatId': msg.get('chatId', '')} for msg in
                        r]
            return {'totalMessages': len(r), 'first100': first100}

    def clear_message_q(self):
        url = self.url + '/ClearMessagesQueue/{}'.format(self.token)

        headers = {
            'Content-Type': 'application/json'
        }

        return requests.get(url=url, headers=headers).json()

    def create_group(self, branch_name, phones):
        """Создание группы в WA ('messageText' пока не работает)"""
        url = self.url + '/CreateGroup/{}'.format(self.token)

        for phone in phones:
            if '-' in phone:
                phone += '@g.us'
            else:
                phone += '@c.us'

        params = {
            'groupName': f'Отзывы {branch_name}'[:25],
            'chatIds': phones,
        }

        r = requests.post(url=url, json=params).json()
        if r.get('created', False) and 'chatId' in r:
            return r['chatId']
        else:
            return False

    def set_group_admin(self, groupId, phone):
        """Добавление прав админа в группе"""
        url = self.url + '/SetGroupAdmin/{}'.format(self.token)

        if '-' in phone:
            phone += '@g.us'
        else:
            phone += '@c.us'

        params = {
            'groupId': groupId,
            'participantChatId': phone,
        }
        r = requests.post(url=url, json=params).json()

        if r.get('setGroupAdmin', False):
            return True
        else:
            return False


def create_msg_caption(green_msg):
    msg = green_msg['downloadUrl']
    caption = green_msg.get('caption', '')
    if caption is None:
        caption = ''
    return msg, caption
