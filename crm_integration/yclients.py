from datetime import datetime, timedelta

from configs import config

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pytz
from loguru import logger

moscow = pytz.timezone('Europe/Moscow')


def market_info(text, event_type):
    if event_type == 'activation':
        log_path = '/home/teman77/botsarmy/logs/market/activations.log'
    elif event_type == 'payment':
        log_path = '/home/teman77/botsarmy/logs/market/payments.log'
    elif event_type == 'refund':
        log_path = '/home/teman77/botsarmy/logs/market/payments.log'

    logger.remove()
    logger.add(log_path, format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def confirm_info(text):
    log_path = '/home/teman77/botsarmy/logs/yclients/confirm/confirmations.log'
    logger.remove()
    logger.add(log_path, format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def get_session():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


user = config.yclients_user
bearer = config.yclients_bearer


class Record:
    def __init__(self, CRM_data):
        self.branch = CRM_data['branch']
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            # 'Accept': 'application/vnd.yclients.v2+json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }
        self.CRM_data = CRM_data

    def get_record(self, record_id='', client_id=None, short_link_token=False):
        url = self.url + f'record/{self.branch}/{record_id}'
        params = {}
        if client_id is not None:
            params.update({'client_id': client_id})
        if short_link_token:
            params['short_link_token'] = 1
        res = get_session().get(url=url, headers=self.headers, params=params, timeout=1)
        return res.json()

    def get_all_for_today(self):
        """
        Returns all records for the day for the specified branch
        :return: json
        :format:
        {count: int (count recs), data: [{record_data}]}
        """
        today = str(datetime.now())[:10]
        url = self.url + 'records/{}'.format(self.branch)
        params = {
            'start_date': today,
            'end_date': today,
            'count': 200
        }
        r = get_session().get(url=url, headers=self.headers, params=params, timeout=1)
        return r.json()

    def get_for_date(self, date):
        """
        Returns all records for the date for the specified branch
        :param date:
        :return: json
        :format:
        {count: int (count recs), data: [{record_data}]}
        """

        url = self.url + 'records/{}'.format(self.branch)
        params = {
            'start_date': date,
            'end_date': date,
            'count': 200
        }

        recs = get_session().get(url=url, headers=self.headers, params=params, timeout=1)
        return recs.json()

    def get_for_period(self, start_date='', end_date='', client_id=None, short_link_token=True):
        """
        Returns all records for the period for the specified branch
        :param start_date:
        :param end_date:
        :param client_id:
        :param short_link_token:
        :return: json
        :format:
        {count: int (count recs), data: [{record_data}]}
        """
        url = self.url + 'records/{}'.format(self.branch)

        records = []
        rec_ids = []

        params = {
            'start_date': start_date,
            'end_date': end_date,
            'count': 200,
            'page': 0
        }

        if client_id is not None:
            params.update({'client_id': client_id})

        if short_link_token:
            params['short_link_token'] = 1

        with get_session().get(url=url, params=params, headers=self.headers, stream=True, timeout=1) as r:
            if r.json().get('count') is None:
                return False
            pages = int(r.json()['count'] / 200) + 1
            for rec in r.json()['data']:
                if rec['id'] not in rec_ids:
                    records.append(rec)
                    rec_ids.append(rec['id'])

        if pages > 1:
            for n in range(1, pages + 1):

                params = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'page': n,
                    'count': 200
                }
                if client_id is not None:
                    params.update({'client_id': client_id})

                with get_session().get(url, params=params, headers=self.headers, stream=True, timeout=1) as r:

                    for rec in r.json()['data']:

                        if rec['id'] not in rec_ids:
                            records.append(rec)
                            rec_ids.append(rec['id'])

        return {'count': len(r.json()['data']), 'data': records}
        # recs = get_session().get(url=url, headers=self.headers, params=params)
        # return recs.json()

    def confirm(self, record_id, staff_id, services, client, date_time, seance_length, activity_id=0, save_if_busy=True,
                send_sms=False, attendance=2):

        url = self.url + 'record/{}/{}'.format(self.branch, record_id)

        params = {
            'staff_id': staff_id,
            'services': services,
            'client': client,
            'datetime': str(date_time),
            'seance_length': seance_length,
            'save_if_busy': save_if_busy,
            'send_sms': send_sms,
            'attendance': attendance
        }
        if activity_id != 0:
            params.update({'activity_id': activity_id})

        n = 0
        while True:
            try:
                r = get_session().put(url=url, json=params, headers=self.headers, timeout=1)
                confirm_info(f'{self.branch} {client["phone"]} {r.json()}')
                return r.json()
            except Exception as e:
                n += 1
                if n > 10:
                    print(f'error: {str(e)}')
                    print(f'ycl.py fail to confirm rec with params: {params}')
                    return False


class Client:
    def __init__(self, CRM_data):
        self.CRM_data = CRM_data
        self.branch = CRM_data['branch']
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }

    def get_by_id(self, client_id):
        url = self.url + 'client/{}/{}'.format(self.branch, client_id)

        r = get_session().get(url=url, headers=self.headers, timeout=1)
        return r.json()

    def get_info_by_phone(self, phone):
        """Возвращает полную информацию о клиенте по номеру телефона"""

        url = self.url + 'clients/{}'.format(self.branch)
        params = {
            'phone': phone
        }
        data = get_session().get(url=url, headers=self.headers, params=params, timeout=1).json()

        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]
        else:
            return None

    def get_all_with_birthdays_for_period(self, start_date, end_date=''):

        url = self.url + 'company/{}/clients/search'.format(self.branch)

        params = {
            'page_size': 200,
            'fields': ['id', 'phone', 'name', 'visits_count'],
            'filters': [
                {'type': 'birthday',
                 'state': {'from': start_date, 'to': end_date}}
            ]
        }
        return get_session().post(url=url, json=params, headers=self.headers).json()

    def get_staff(self, staff=''):
        url = self.url + 'company/{}/staff/{}'.format(self.branch, staff)
        r = requests.get(url=url, headers=self.headers, timeout=5)
        return r.json()

    def save_clients(self, params):
        """
        Saves numbers to the customer's database in yclients
        :param params: [{'name': str, 'phone': str}]
        :return: json (action result)
        """
        url = self.url + 'clients/{}/bulk'.format(self.branch)
        data = get_session().post(url=url, json=params, headers=self.headers, timeout=10)
        dj = data.json()
        if ('success' in dj and len(dj['data']['created']) > 0) or ('created' in dj and len(dj['created']) > 0):
            return {'success': True}
        else:
            return {'success': False}

    def get_all_clients_base(self, filters):
        """
        Searches for data by the specified filter in the customer database in yclients
        :param filters: dict (filter params in ycl docks)
        :return: dict with fields from params['fields']
        """
        url = self.url + 'company/{}/clients/search'.format(self.branch)
        params = {
            'page_size': 200,
            'fields': ['id', 'phone', 'name', 'visits_count'],
            'operation': 'OR',
            'filters': filters
        }
        r = get_session().post(url=url, json=params, headers=self.headers, timeout=10)
        return r.json()


class Group:
    """Класс для операций на уровне группы филиалов"""

    def __init__(self, CRM_data):
        self.group_id = CRM_data['group_id']
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.yclients.v2+json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }

    def get_client_group_info(self, client_phone):
        """ ищет клиента по сети салонов, если не находит, то возвращает False """
        url = self.url + f'group/{self.group_id}/clients/'
        r = get_session().get(url=url, headers=self.headers, params={'phone': client_phone}, timeout=1)
        if r.json()['success']:
            return r.json()
        else:
            return False


class Loyalty:

    def __init__(self, CRM_data):
        self.branch = CRM_data['branch']
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.yclients.v2+json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }

    def get_cards_by_group_id(self, group_id):
        url = self.url + f'user/loyalty_cards/{group_id}'
        return get_session().get(url=url, headers=self.headers, timeout=1)

    def get_cards_by_company_id(self):
        url = self.url + f'loyalty/card_types/salon/{self.branch}'
        return get_session().get(url=url, headers=self.headers, timeout=1).json()

    def get_client_cards(self, client_id):
        url = self.url + f'loyalty/client_cards/{client_id}'
        return get_session().get(url=url, headers=self.headers, timeout=2).json()

    def get_loyal_transactions_for_visit(self, visit_id):
        url = self.url + f'visit/loyalty/transactions/{visit_id}'
        return get_session().get(url=url, headers=self.headers, timeout=2).json()

    def client_have_abonement(self, client_phone):
        """Проверяет есть ли активный абонемент у клиента, возвращает True или False"""
        url = self.url + 'loyalty/abonements/'
        params = {
            'company_id': int(self.branch),
            'phone': int(client_phone)
        }
        r = requests.get(url=url, headers=self.headers, params=params, timeout=1).json()
        if r['success'] and r['meta']['count'] > 0:
            return True
        return False


class Marketplace:

    def __init__(self, CRM_data):
        self.app_id = config.yclients_app_id
        self.url = 'https://api.yclients.com/api/v1/'
        self.branch_id = CRM_data['branch']
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.yclients.v2+json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }

    def payment(self, payment_sum, period_from, period_to):
        url = 'https://api.yclients.com/marketplace/partner/payment'

        # переводим дату подписки на следующий день
        period_to += timedelta(days=1)

        data = {
            'salon_id': self.branch_id,
            'application_id': self.app_id,
            'payment_sum': payment_sum,
            'payment_date': str(datetime.now(moscow))[:19],
            'period_from': str(period_from)[:19],
            'period_to': str(period_to.replace(hour=0, minute=1))[:19]
        }
        result = get_session().post(url=url, json=data, headers=self.headers)
        print('yclients market payment', result, data, result.text)
        market_info(f'{result} {data} {result.text}', 'payment')
        return result.json()

    def refund_payment(self, payment_id):
        url = f'https://api.yclients.com/marketplace/partner/payment/refund/{payment_id}'

        result = get_session().post(url=url, headers=self.headers)
        print('yclients market refund payment', result, result.text)
        market_info(f'{result} {result.text}', 'refund')
        if result.status_code == 200:
            return True
        else:
            return result.json()

    def get_data(self):
        url = f'https://api.yclients.com/marketplace/salon/{self.branch_id}/application/3'
        result = get_session().get(url=url, headers=self.headers)
        print(result.json())

# crm_data = {'name': 'yclients', 'branch': '501945'}
# print(Marketplace(crm_data).get_data())

class Webhook:

    def __init__(self, CRM_data):
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.yclients.v2+json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }
        self.CRM_data = CRM_data

    def get_webhook_settings(self):
        """ Получает данные о настройках вебхуков """
        url = self.url + f'hooks_settings/{self.CRM_data["branch"]}'
        r = get_session().get(url=url, headers=self.headers)
        assert r.status_code in [200, 201] and r.json()[
            'success'], f'невозможно получить вебхук для филиала {self.CRM_data["branch"]} ({self.CRM_data["name"]})'
        return r.json()

    def post_webhook_settings(self, settings):
        """ Изменяет данные о настройках вебхуков """
        url = self.url + f'hooks_settings/{self.CRM_data["branch"]}'

        r = get_session().post(url=url, headers=self.headers, json=settings)
        assert r.status_code in [200, 201] and r.json()[
            'success'], f'невозможно установить вебхук для филиала {self.CRM_data["branch"]} ({self.CRM_data["name"]})'
        return r


class Services:
    def __init__(self, CRM_data):
        self.branch = CRM_data['branch']
        self.url = 'https://api.yclients.com/api/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.yclients.v2+json',
            'Authorization': 'Bearer {}, User {}'.format(bearer, user)
        }

    # Объеденить в класс Services
    def get_service_category(self, service_id):
        url = f'https://api.yclients.com/api/v1/company/{self.branch}/services/{service_id}'

        r = get_session().get(url=url, headers=self.headers)

        assert r.status_code in [200, 201] and r.json()['success'] == True, ' for branch {} service_id {}\n\n{}'.format(
            self.branch, service_id, r.text)

        return r.json()

    # Объеденить в класс Services
    def get_all_branch_services(self):
        url = f'https://api.yclients.com/api/v1/company/{self.branch}/services/'

        r = get_session().get(url=url, headers=self.headers)
        if r.json().get('success', False):
            return r.json()
        else:
            return None


def auth(login, password):
    url = 'https://api.yclients.com/api/v1/auth'

    headers = {
        'Accept': 'application/vnd.yclients.v2+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {!s}'.format(bearer)
    }
    params = {
        'login': login,
        'password': password
    }

    return get_session().post(url=url, json=params, headers=headers)

# новый метод api
# POST /api/v1/auth изменить на POST /api/v1/booking/auth

# print(auth('79255988292', 'xxx').json())
