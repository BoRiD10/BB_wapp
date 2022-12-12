import time
import traceback
from datetime import datetime, timedelta
from random import choice
import requests
from dateutil.parser import parse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from loguru import logger

from configs import config_beauty, config
from telegram import Bot
from wapp import GreenApi


def utils_error(text):
    logger.remove()
    logger.add('botsarmy/logs/utilities/utils_error.log', format='{time} {level} {message}',
               level='ERROR', rotation='00:00', compression='tar.xz')
    logger.error(text)


def utils_info(obj, function):
    text = f'{function}: {obj["bot_client"]} {obj["wapp"]["instanceId"]} {obj["phone"]} {obj["task_queue"]} {obj["body"][0:30]}'
    logger.remove()
    logger.add('botsarmy/logs/utilities/utils_info.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def check_wapp_logs(text):
    logger.remove()
    logger.add('botsarmy/logs/utilities/wapp/check_wapp.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def get_digits_from_string(string, stop=[]):
    digits = ''

    for s in string:

        if s in stop:
            return digits

        try:
            int(s)
            digits += s
        except:
            pass

    return digits


def insert_keys_into_templates(keys, template, note_before='', randomize=True):
    """ вставляет ключи и рандомизирует текст """
    template = template.format(
        name=keys['name'],
        day_month=keys['day_month'],
        day_of_week=keys['day_of_week'],
        start_time=keys['start_time'],
        end_time=keys['end_time'],
        master=keys['master'],
        price=keys['price'],
        filial=keys['filial_name'],
        note_before=note_before,
        client_phone=keys['client_phone'],
        services=keys['services'],
        review_link=keys['review_link'],
        bonus_add=keys['bonus_add'],
        bonus_withdraw=keys['bonus_withdraw'],
        bonus_balance=keys['bonus_balance'],
        time_master=keys['time_master'],
        time_service=keys['time_service'],
        record_link=keys['record_link']
    )

    if randomize:
        return randomize_text(template)
    else:
        return template


def get_utc_timestamp_from_string(str_date):
    if type(str_date) is str:
        date_time = datetime.strptime(str_date[:19], "%Y-%m-%dT%H:%M:%S")  # + timedelta(hours= int(str_date[20:22]))
        return date_time
    else:
        return str_date


def randomize_text(text):
    letters = {
        'а': ['a', 'а'],
        'А': ['А', 'A'],
        'В': ['B', 'В'],
        'С': ['С', 'C'],
        'с': ['с', 'c'],
        'Е': ['Е', 'E'],
        'е': ['е', 'e'],
        'Н': ['Н', 'H'],
        'К': ['К', 'K'],
        'М': ['М', 'M'],
        'О': ['О', 'O'],
        'о': ['о', 'o'],
        'Р': ['Р', 'P'],
        'Т': ['Т', 'T'],
        'х': ['х', 'x'],
        'Х': ['Х', 'X'],
        'у': ['у', 'y']
    }

    string = text
    string = list(string)

    for n, i in enumerate(string):
        if i in letters:
            string[n] = choice(letters[i])

    return ''.join(string)


def create_msg_for_control_bot(message, instanceId, branch_name, enable_reply_in_bot=False):
    """ Создаёт текст сообщения для отправки в телеграм копии вотсап-сообщения """

    #  удаляем из текста символы < > чтобы не падала отправка в телегу с markdown='HTML'
    message['body'] = message['body'].replace('<', '').replace('>', '')
    sender_name = message['sender_name'].replace('<', '').replace('<', '')
    warning = ('\n<i>Сообщение в трансляции обрезано в связи с ограничениями со стороны Telegram.'
               '\nНе переживайте, клиентам сообщения отправляются полностью!</i>')
    if 'caption' in message and message['caption'] is not None:
        message['caption'] = message['caption'].replace('>', '').replace('<', '')

    if not message['from_me']:
        icon = '👇'
    else:
        icon = '👆'
    client_phone = get_digits_from_string(message['phone'])
    icon += f'<b>{branch_name}</b> {sender_name} #t{client_phone}'

    if message['channel'] == 'telegram':
        icon += ' (Telegram)'
    elif message['channel'] == 'wapp':
        icon += ' (WhatsApp)'

    if enable_reply_in_bot and not message['from_me']:
        icon += ' #i{}'.format(instanceId)

    if message['is_forwarded'] == 1:
        icon += '\n' + '<i>Пересланное сообщение</i>'

    if message['type'] in ['chat', 'buttons_response']:
        msg = icon + '\n\n' + message['body'][:3000]
        if len(message['body']) > 3000:
            msg += warning
    else:
        if 'caption' in message and message['caption'] is not None:
            msg = icon + '\n\n' + message['caption'][:800]
            if len(message['caption']) > 800:
                msg += warning
        else:
            msg = icon

    return msg


def hide_phone_in_translation_msg(text):
    """Скрывает номер телефона из сообщения для трансляции."""
    msg = text.replace(text[text.index('#'):text.index('(')], '#номер скрыт ')
    return msg


def report_exception(traceback_msg, r=None):
    if len(traceback_msg) > 3700:
        traceback_msg = traceback_msg[:3700]
    msg = '```\n' + traceback_msg + '\n```'
    utils_error(msg)
    to_send = [msg]
    if r is not None:
        utils_error(str(r))
        mark_r = str(r).replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
        to_send.append(mark_r)

    for m in to_send:
        Bot(config.bb_dev_bot_token).send_message(-433714683, m)

    return 'ok'


def get_tlg_token(conn, account):
    if 'partner_id' in account['settings']:
        token_find = conn[config_beauty.bb_db]['partners_bot'].find_one(
            {'partner_id': account['settings']['partner_id']})
        if token_find is not None:
            token = token_find['tlg_token']
        else:
            report_exception(
                f'Не найден токен для partner_id: {account["settings"]["partner_id"]} в send_tmsg_to_queue')
            return 'No token for partner id'
    else:
        token = config.beauty_bot_static_token
    return token


def autogen_channels(settings, channels):
    if 'send_tg' in settings and not settings['send_tg']:
        channels.remove('tg')
    if 'send_tg' in settings and settings['send_tg'] and 'tg' not in channels:
        channels = ['WA', 'tg', 'sms']
    if 'send_WA' in settings and not settings['send_WA']:
        channels.remove('WA')
    return channels


'''ОТПРАВКА СООБЩЕНИЙ'''


def send_message_to_queue(conn, type, bot_client, account, phone, text, send_time, sms_text='', caption=None,
                          buttons=False, from_trello=False, options=[]):
    """Функция определяет канал отправки и создает объект сообщения"""
    if send_time == 'now':
        send_time = time.time()
    elif send_time == 'urgent':
        send_time = time.time() - 20000
    else:
        send_time = time.time()

    channels = account['settings']['priority_channels'] if 'priority_channels' in account['settings'] else ['WA', 'sms']
    channels = autogen_channels(account['settings'], channels)

    data = send_message_WA(type, bot_client, account, phone, text, send_time, caption, from_trello, options)

    for channel_name in channels:

        if channel_name == 'WA':
            if 'g.us' not in phone:
                type_message = choose_check_wapp(conn, data)
            else:
                type_message = 'wapp'

            if type_message == 'wapp':
                utils_info(data, 'send_msg_WA')
                # для дева
                if config_beauty.development == 0:
                    return conn['db1']['message_queue2'].insert_one(data)
                else:
                    return conn['db1']['message_queue1'].insert_one(data)
        elif channel_name == 'sms':
            utils_info(data, 'send_msg_sms')
            send_sms_to_queue(conn, bot_client, account, phone, text, send_time, sms_text='')
            return 'send_sms'


def send_message_WA(type, bot_client, account, phone, text, send_time, caption=None, from_trello=False, options=[]):
    """Создаем объект сообщения для отправки в WA"""

    data = {
        'bot_client': bot_client['name'],
        'wapp': account['chat_api'],
        'type': type,
        'phone': phone,
        'body': text,
        'time': send_time
    }

    if 'task_queue' in account['settings']:
        data['task_queue'] = account['settings']['task_queue']

    if caption is not None:
        data['caption'] = caption

    if from_trello:
        data['from_trello'] = True

    if len(options) > 0:
        data['options'] = options

    return data


def choose_check_wapp(conn, data):
    """Функция проверяет наличие номера в базе"""
    wapp_ok_phones = conn['tech_db']['all_wapps'].count_documents({'phone': data['phone']})
    # если номера нет в списке номеров
    if wapp_ok_phones == 0:
        return check_wapp(conn, data)
    else:
        return 'wapp'


def check_wapp(conn, data):
    """
    Функция проверяет возможность отправки в WA
    """
    phone = get_digits_from_string(data['phone'])
    try:
        check = GreenApi(data['bot_client'], data['wapp']).check_exist(phone)
        # есть вотсап для green-api
        if check.get('existsWhatsapp', False):
            conn['tech_db']['all_wapps'].insert_one({'phone': phone})
            return 'wapp'
        else:
            check_wapp_logs(f'Result check wapp for {data["phone"]} inst {data["wapp"]["instanceId"]}: {check}')
            return 'sms'
    except:
        utils_error(f'Ошибка при проверке наличия номера {str(traceback.format_exc())}, сообщение {str(data)}')
        return double_check_wapp(conn, phone)


def double_check_wapp(conn, phone):
    try:
        check = GreenApi('BB_tech', config.wapps['bb_wapp']).check_exist(phone)
        # есть вотсап для green-api
        if check.get('existsWhatsapp', False):
            conn['tech_db']['all_wapps'].insert_one({'phone': phone})
            return 'wapp'
        else:
            return 'sms'
    except:
        utils_error(f'Ошибка при повторной проверке наличия номера {str(traceback.format_exc())}, номер {phone}')
        return 'wapp'


def send_tmsg_to_queue(conn, bot_client, user_id, body, send_time, type='chat', sms_text='', reply_markup='',
                       caption=None, pin=False, cached=False):
    if send_time == 'now':
        send_time = time.time()

    token = get_tlg_token(conn, bot_client)

    data = {
        'bot_client': bot_client['name'],
        'token': token,
        'type': type,
        'user_id': user_id,
        'body': body,
        'time': send_time,
        'cached': cached
    }

    if sms_text != '':
        data.update({'sms_text': sms_text})

    if caption is not None:
        data['caption'] = caption

    # if pin != False:
    #     data.update({'pin_message': pin})
    #     return conn['tech_db']['test_status_msg'].insert_one(data)

    if config_beauty.development == 0:
        conn[config_beauty.bb_db]['tmsg_queue1'].insert_one(data)
    if config_beauty.development == 1:
        conn[config_beauty.bb_db]['tg_queue2'].insert_one(data)

    return 'done'


def send_sms_to_queue(conn, bot_client, account, phone, text, send_time, sms_text=''):
    """Функция вставляет объект сообщения в коллекцию очереди сообщений на отправку"""
    if send_time == 'now':
        send_time = time.time()
    elif send_time == 'urgent':
        send_time = time.time() - 20000
    else:
        send_time = time.time()

    data = {
        'bot_client': bot_client['name'],
        'wapp': account['chat_api'],
        'type': 'text',
        'phone': phone,
        'body': text,
        'time': send_time
    }

    if sms_text != '':
        data.update({'sms_text': sms_text})

    if config_beauty.development == 0:
        return conn['db1']['sms_queue'].insert_one(data)
    else:
        return conn['db1']['sms_queue_dev'].insert_one(data)


def get_session():
    """
    Создаёт и возвращает сессию
    """
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def account_paid(account):
    """
    Проверяет акк на оплаченность с учётом часового пояса клиента, возвращает True/False
    """
    if 'pay_period' in account and account['pay_period'] != '':
        paid_till = parse(account['pay_period'])
        client_date = datetime.now() + timedelta(hours=account['settings']['time_to_msk'] + 3)

        if paid_till.date() >= client_date.date():
            return True

        else:
            return False
    else:
        return True


def check_client_name(name_from_yclient, names=None, account=None):
    """Функция ищет имя по списку имён, возвращает имя, а если не находит, возвращает Уважаемый клиент"""

    default_name = 'Уважаемый клиент'

    for locale in config_beauty.locale:
        if account is not None and account['id'] in locale['acc_id']:
            if 'default_name' in locale:
                default_name = locale['default_name']

    if names is None:
        n = 0
        while n < 3:
            try:
                with open(config_beauty.names_path, 'r', encoding='utf-8') as file:
                    read = file.read().splitlines()
                names = [x.lower() for x in read]
                n = 10
            except:
                n += 1
                tb = traceback.format_exc(chain=False)
                msg = f'get name error\n' + '```\n' + tb + '\n```'
                Bot(config.bb_dev_bot_token).send_message(config_beauty.tg_err_group_id, msg)

    try:
        all_word = name_from_yclient.split()
        if len(all_word) == 0:
            return default_name

        elif len(all_word) == 1:
            name = ''.join([i for i in all_word[0] if i.isalpha()])
            if name == '' or name.lower() not in names:
                return default_name
            return name

        else:
            for word in all_word:
                # убираем всё кроме букв
                word = ''.join([i for i in word if i.isalpha()])
                if len(word) > 2 and word.lower() in names:
                    return word
    except:
        return default_name

    return default_name
