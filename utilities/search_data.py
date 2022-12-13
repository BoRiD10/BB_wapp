import calendar
import traceback
from datetime import datetime, timedelta
from loguru import logger

from configs import config_beauty, config
from crm_integration import target
from mongo import get_conn
from telegram import Bot
import utilities.utils as ut


def yclients_error(text):
    logger.remove()
    logger.add('BB_wapp/logs/yclients/yclients_error.log', format='{time} {level} {message}',
               level='ERROR', rotation='00:00', compression='tar.xz')
    logger.error(text)


def yclients_short_link_token(text):
    logger.remove()
    logger.add('BB_wapp/logs/testing_short_links/keys_create.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.error(text)


# ПО возможности зарефакторить
def get_record_keys(account, r, multiple_recs=None, message='', conn=None):
    if multiple_recs is None:
        if type(r['data']['datetime']) is str:
            r['data']['datetime'] = ut.get_utc_timestamp_from_string(r['data']['datetime'])
    else:
        for rec in multiple_recs:
            if type(rec['datetime']) is str:
                rec['datetime'] = ut.get_utc_timestamp_from_string(rec['datetime'])

    keys = Keys(conn, account, record=r, multiple_recs=multiple_recs)
    date_time = r['data']['datetime']
    client = r['data']['client']

    dow = calendar.weekday(date_time.year, date_time.month, date_time.day)
    day_of_week = keys.days[dow]
    month = keys.months[str(date_time.month)]
    day_month = '{} {}'.format(date_time.day, month)

    name = keys.get_date_names()
    master = keys.get_master_name()
    price = keys.get_price()
    services = keys.get_service()
    start_time, end_time, start_end_time = keys.start_end_time()

    if 'goods_transactions' in r['data']:
        for g in r['data']['goods_transactions']:
            price += g['cost'] * abs(g['amount'])

    data = {
        'name': name,
        'day_month': day_month,
        'day_of_week': str(day_of_week),
        'start_time': start_time,
        'end_time': end_time,
        'start_end_time': start_end_time,
        'master': master,
        'price': price,
        'filial_name': account['CRM_data']['branch_name'],
        'client_phone': ut.get_digits_from_string(client['phone']),
        'client_id': client['id'],
        'services': services,
        'time_service': '',
        'time_master': '',
        'review_link': '',
        'record_link': '',
        'bonus_add': '',
        'bonus_withdraw': '',
        'bonus_balance': ''
    }

    # если нужна информация о бонусах, добавляем её в ключи
    if '{bonus' in message:
        bonus_plus, bonus_minus, balance = keys.get_bonus()
        data.update({
            'bonus_add': bonus_plus,
            'bonus_withdraw': bonus_minus,
            'bonus_balance': balance
        })

    # добавляем специальный ключ time_master, который позволяет показывать записи так: 👉 в 14:00 - Ильясова Марианна
    if 'time_master' in message:
        time_master = keys.get_time_master()
        data['time_master'] = time_master

    if '{time_service}' in message:
        time_service = keys.time_service(services)
        data['time_service'] = time_service

    if '{review_link}' in message:
        review_link = keys.get_review_link()
        data['review_link'] = review_link

    if '{record_link}' in message:
        record_link = keys.get_record_link()
        data['record_link'] = record_link

    return data


class Keys:
    def __init__(self, conn, account, record, multiple_recs=None):
        self.conn = conn
        self.account = account
        self.record = record
        self.multiple_recs = multiple_recs
        self.default_name, self.days, self.months = self.get_date_names()

    def get_date_names(self):
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        months = {'1': 'января', '2': 'февраля', '3': 'марта', '4': 'апреля', '5': 'мая', '6': 'июня', '7': 'июля',
                  '8': 'августа', '9': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'}
        default_name = 'Уважаемый клиент'

        # проверка на локализацию
        for locale in config_beauty.locale:
            if self.account['id'] in locale['acc_id']:
                if 'months' in locale:
                    months = locale['months']
                if 'days_of_week' in locale:
                    days = locale['days_of_week']
                if 'default_name' in locale:
                    default_name = locale['default_name']

        return default_name, days, months

    def get_names(self):
        # проверка и поиск имени
        name = self.record['data']['client']['name']
        if name != '':

            try:
                name = ut.check_client_name(name)
            except:
                tb = traceback.format_exc(chain=False)
                msg = f'get name error\n' + '```\n' + tb + '\n```'
                Bot(config.bb_dev_bot_token).send_message(config_beauty.tg_err_group_id, msg)

            if not name[0].isupper():
                name = name[0].upper() + name[1:]
            else:
                name = name[0].upper() + name[1:].lower()
        else:
            name = self.default_name
        return name

    def get_master_name(self):
        if self.multiple_recs is None:
            master = self.record['data']['staff']['name']
        else:
            master = ', '.join([x['staff']['name'] for x in self.multiple_recs if 'name' in x['staff']])
        return master

    def get_price(self):
        price = 0
        if self.multiple_recs is None:
            for service in self.record['data']['services']:
                if int(service['cost_per_unit'] * service['amount']) == service['cost']:
                    price += int(service['cost_per_unit'] * service['amount'])
                else:
                    price += int(service['cost'])
        else:
            for records in self.multiple_recs:
                for service in records['services']:
                    if int(service['cost_per_unit'] * service['amount']) == service['cost']:
                        price += int(service['cost_per_unit'] * service['amount'])
                    else:
                        price += int(service['cost'])
        return price

    def get_service(self):
        services = ''
        if self.multiple_recs is not None:
            for recs in self.multiple_recs:
                for i in recs['services']:
                    services += '▫️' + i['title'] + '\n'
        else:
            for i in self.record['data']['services']:
                services += '▫️' + i['title'] + '\n'
        return services

    def start_end_time(self):
        date_time = self.record['data']['datetime']
        seance_lenght = self.record['data']['seance_length']
        now = datetime.now()
        record_time = now.replace(hour=date_time.hour, minute=date_time.minute)
        if self.multiple_recs is None:
            start_time = date_time.strftime('%Y-%m-%dT%H:%M:%S')[11:16]
            length_seconds = seance_lenght
            end_time = (record_time + timedelta(0, int(length_seconds))).strftime('%Y-%m-%dT%H:%M:%S')[11:16]
            start_end_time = f'{start_time}-{end_time}'
        else:
            repeat_times = []
            s_e_repeat_times = []
            end_repeat_times = []
            for rec in self.multiple_recs:
                str_datetime = rec['datetime'].strftime('%Y-%m-%dT%H:%M:%S')[11:16]
                length_seconds = rec['data']['seance_length']
                end_time = (record_time + timedelta(0, int(length_seconds))).strftime('%Y-%m-%dT%H:%M:%S')[11:16]
                if str_datetime not in repeat_times:
                    repeat_times.append(str_datetime)
                    end_repeat_times.append(end_time)
                    s_e_repeat_times.append(f'{str_datetime}-{end_time}')
            start_time = ', '.join(repeat_times)
            end_time = ', '.join(end_repeat_times)
            start_end_time = ', '.join(s_e_repeat_times)

        return start_time, end_time, start_end_time

    def get_bonus(self):
        bonus_plus = 0
        bonus_minus = 0
        crm_data = self.account['CRM_data']
        transactions = target.Loyaltys(crm_data).get_loyal_transactions_for_visit(self.record['data']['visit_id'])[
            'data']
        for tr in transactions:
            if 'type' in tr and 'сертифика' not in tr['type']['title'].lower() and 'абонеме' not in tr['type'][
                'title'].lower() and 'скидка' not in tr['type']['title'].lower():
                if not tr['is_loyalty_withdraw']:
                    bonus_plus += tr['amount']
                else:
                    bonus_minus += tr['amount']

        cards = target.Loyaltys(crm_data).get_client_cards(self.record['data']['client']['id'])['data']

        balance = 0
        for card in cards:
            balance += card['balance']

        return int(bonus_plus), int(bonus_minus), int(balance)

    def get_time_master(self):
        if self.multiple_recs is None:
            str_datetime = self.record['data']['datetime'].strftime('%Y-%m-%dT%H:%M:%S')
            time_master = ' '.join(['👉', 'в', str_datetime[11:16], '-', self.record['data']['staff']['name']])

        else:
            repeat_times = []
            for rec in self.multiple_recs:
                str_datetime = rec['datetime'].strftime('%Y-%m-%dT%H:%M:%S')
                repeat_times.append('{} {} {} {} {}'.format('👉', 'в', str_datetime[11:16], '-', rec['staff']['name']))
            time_master = '\n'.join(repeat_times)
        return time_master

    def time_service(self, services):
        time_service = ''
        if self.multiple_recs is None:
            str_datetime = self.record['data']['datetime'].strftime('%Y-%m-%dT%H:%M:%S')
            for i in self.record['data']['services']:
                services += '▫️' + i['title'] + '\n'
            time_service = ' '.join(['👉', 'в', str_datetime[11:16], ':\n', services])
        else:
            for rec in self.multiple_recs:
                str_datetime = rec['datetime'].strftime('%Y-%m-%dT%H:%M:%S')
                for i in rec['data']['services']:
                    services += '▫️' + i['title'] + '\n'
                time_service = ' '.join(['👉', 'в', str_datetime[11:16], ':\n', services])
        return time_service

    def get_review_link(self):
        if self.multiple_recs is None:
            review_link = get_review_link(self.conn, self.record, self.account)
        else:
            link_lst = []
            for r in self.multiple_recs:
                rev_link = get_review_link(self.conn, r, self.account)
                if rev_link is not None:
                    link_lst.append(rev_link)
            review_link = '\n'.join(link_lst)
        return review_link

    def get_record_link(self):
        record_link = ''
        rec_link_base = config_beauty.rec_link_base[self.record['name']]
        if 'short_link_token' in self.record['data']:
            record_link = rec_link_base + self.record['data']['short_link_token']
        else:
            token = get_record_token(self.account, self.record)
            if 'error' not in token:
                record_link = rec_link_base + token
                # добавляем в базу для будущих шаблонов
                if self.conn is None:
                    conn = get_conn()
                else:
                    conn = self.conn

                conn[config_beauty.bb_db]['records'].update_many(
                    {'company_id': int(self.record['company_id']), 'resource_id': int(self.record['data']['id'])},
                    {'$set': {'data.short_link_token': token}})
                # yclients_short_link_token(f'ycl.py short_token NOT found: {token} {str(data["record_link"])}')
            else:
                yclients_short_link_token(f'ycl.py short_token ERROR found: {self.record["data"]["id"]} {token}')

        return record_link


def get_short_link_token(crm_data, record_id):
    r = target.Records(crm_data).get_record(record_id, short_link_token=True)

    try:
        return r['short_link_token']
    except:
        return False


def get_record_token(acc, record):
    """Получает токен отзыв или создание записи в yclients"""

    token = get_short_link_token(acc['CRM_data'], record['data']['id'])
    if token:
        return token
    else:
        return {'error': f'error getting token in yclients.py: {str(token)}'}


def get_review_link(conn, r, account):
    rev_link_base = config_beauty.rev_link_base[r.get('name', 'yclients')]
    if 'data' not in r:
        r = {'data': r}
    if 'short_link_token' in r['data']:
        return rev_link_base + r['data']['short_link_token']
    else:
        token = get_record_token(account, r)
        if 'error' not in token:
            link = rev_link_base + token
            if conn is None:
                conn = get_conn()
            conn[config_beauty.bb_db]['records'].update_one(
                {'company_id': int(r['data']['company_id']), 'resource_id': int(r['data']['id'])},
                {'$set': {'data.short_link_token': token}})
            return link
        else:
            yclients_short_link_token(
                f'ycl.py short_token ERROR found: {r["data"]["id"]} {token}')
        return ''


def confirm_client_recs_for_date(crm_data, client_id, date, confirm=True):
    recs = target.Records(crm_data).get_for_period(start_date=date, end_date=date, client_id=client_id)
    if not recs or len(recs['data']) == 0:
        yclients_error(f'No recs for {crm_data["branch"]}\n\n{recs}')
        return 'No recs'

    fail_counter = 0
    for rec in recs['data']:
        if rec['attendance'] == -1:
            fail_counter += 1
            continue

        # если в записи несколько одинаковых услуг, нужно переделать 'first_cost' и 'cost_per_unit'
        for s in rec['services']:
            if s['amount'] > 1:
                s['first_cost'] = s['cost_per_unit']

        if confirm:
            r = target.Records(crm_data).confirm(rec['id'], rec['staff']['id'], rec['services'], rec['client'],
                                                 rec['datetime'], rec['seance_length'], activity_id=rec['activity_id'],
                                                 save_if_busy=True, send_sms=False)
        else:
            r = target.Records(crm_data).confirm(rec['id'], rec['staff']['id'], rec['services'], rec['client'],
                                                 rec['datetime'], rec['seance_length'], activity_id=rec['activity_id'],
                                                 save_if_busy=True, send_sms=False, attendance=-1)

    if fail_counter == len(recs['data']):
        return f'No confirm records for {client_id} in {crm_data["branch"]} (attendance: -1)'

    try:
        return r
    except:
        ut.report_exception(str(traceback.format_exc()), str(recs))