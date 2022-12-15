import time
import traceback
from datetime import datetime, timedelta

from bson import ObjectId
from loguru import logger
from pymongo import DESCENDING

import mongo
import utilities.search_data as sd
import utilities.utils as ut
from configs import config_beauty, config_keyboard
from telegram import Bot
from utilities import speech_recognition


def wapp_process_error(text):
    logger.remove()
    logger.add('BB_wapp/logs/wapp_process/wapp_process_error.log', format='{time} {level} {message}',
               level='ERROR', rotation='00:00', compression='tar.xz')
    logger.error(text)


class WappHooksProcess:

    def __init__(self, conn, account, message, phone, instance_id):
        self.conn = conn
        self.message = message
        self.instance_id = instance_id
        self.account = account
        self.phone = phone

    def save_phones_in_db(self):
        try:
            save_phones = self.account['settings'].get('save_phones_ycl', False)
            if save_phones:
                save_phones_data = {
                    'name': self.message['sender_name'],
                    'phone': self.phone,
                    'instanceId': self.instance_id,
                    'acc_id': self.account['id'],
                    'CRM_data': self.account['CRM_data'],
                    'created_at': datetime.now()
                }
                self.conn[config_beauty.bb_db]['save_phones_ycl'].insert_one(save_phones_data)
            else:
                return {'ok': False, 'status': 'save_phones_ycl off'}
        except:
            return {'ok': False, 'status': 'Phone already exist in DB'}
        return {'ok': True, 'status': 'Phone save in DB'}

    def send_translation_message(self):
        # V2 проверяем наличие номера телефона или группы в исключениях, если они там есть, то не отправляем их в бота
        if self.phone in self.account['settings']['phones_dont_show_in_bot']:
            return {'ok': False, 'status': 'Phone in dont_show_list'}

        branch_name = self.account['CRM_data']['branch_name']
        enable_reply_in_bot = False
        cached = False
        if 'enable_reply_in_bot' in self.account['settings'] and self.account['settings']['enable_reply_in_bot']:
            enable_reply_in_bot = True

        # Новый блок с очередью
        if self.message['type'] in ['chat', 'buttons_response']:
            msg = ut.create_msg_for_control_bot(self.message, self.instance_id, branch_name, enable_reply_in_bot)  # +
            caption = ''
        else:
            msg = self.message['body']
            caption = ut.create_msg_for_control_bot(self.message, self.instance_id, branch_name,
                                                    enable_reply_in_bot)  # +
            if self.message['cached']:
                cached = True

        # уведомляем всех кого надо
        kb = config_keyboard.kb
        for tg in self.account['settings']['notify']:
            if tg in self.account['settings'].get('hide_translation_phones', []):
                if caption != '':
                    caption = ut.hide_phone_in_translation_msg(caption)
                else:
                    msg = ut.hide_phone_in_translation_msg(msg)
            try:
                ut.send_tmsg_to_queue(self.conn, self.account, tg, msg, time.time(), type=self.message['type'],
                                      reply_markup=kb, caption=caption, cached=cached)
            except:
                ut.report_exception('send_tmsg_to_queue error ')
                ut.report_exception(str(traceback.format_exc()))

        return {'ok': True, 'status': 'translation message send'}

    def read_message_and_check_flags(self, text):
        """Функция проверяет наличие флагов по каждому сообщению и подтверждает записи"""
        max_messages = 2
        # все флаги сообщений на данный момент
        flag_name = 'confirm_record'
        # добавляем номер телефона клиента
        client_phone = self.message['phone']

        # проверяем на правильность телефона, если неправильный, крутим дальше
        if len(client_phone) < 10 or len(client_phone) > 14:
            return {'ok': False, 'status': 'record not confirmed'}

        # если входящее сообщение было в группу
        if 'g.us' in self.message['chat_id'] or '-' in self.message['chat_id']:
            return {'ok': False, 'status': 'record not confirmed'}

        search_data = {'client_phone': client_phone, 'instanceId': self.instance_id, 'type': flag_name}
        # ищем флаг для данного клиента
        all_flags = list(
            self.conn[config_beauty.bb_db]['flags'].find(search_data).sort('sent_time', DESCENDING).limit(1))

        if len(all_flags) == 0:
            return {'ok': False, 'status': 'record not confirmed'}

        flag = all_flags[0]

        # проверяем на просроченность
        if time.time() - flag['sent_time'] > flag['valid_hours'] * 60 * 60:
            self.conn[config_beauty.bb_db]['flags'].delete_many(
                {'client_phone': client_phone, 'acc_id': flag['acc_id']})
            return {'ok': False, 'status': 'flag not valid'}

        # ищем согласие в тексте
        confirmation = speech_recognition.find_agree_in_text(text)['result']

        # если не подтвердил
        if confirmation == 'declined':
            confirm_or_dicline_rec(self.conn, flag, client_phone, flag_name, confirm=False)

        # если нейтрально
        if confirmation == 'neutral':
            # если было меньше входящих, чем установлено (обычно 2), то просто делаем + 1
            if flag['income_messages'] < max_messages:
                self.conn[config_beauty.bb_db]['flags'].update_one({'client_phone': client_phone, 'instanceId': self.instance_id}, {
                    '$set': {'income_messages': flag['income_messages'] + 1}})
            # если равно максимуму, то удаляем флаг
            else:
                self.conn[config_beauty.bb_db]['flags'].delete_many({'client_phone': client_phone, 'instanceId': self.instance_id})

        # если нашёл согласие в сообщении
        elif confirmation == 'yes':
            confirm_or_dicline_rec(self.conn, flag, client_phone, flag_name, confirm=True)

        return {'ok': True, 'status': 'record confirmed'}

    def check_reply_tmp(self):
        """ проверяет входящее сообщение не ответ ли на рассылку """
        time_sendouts = datetime.now() - timedelta(days=1)

        data = {
            'phone': self.phone,
            'created_at': {'$gte': time_sendouts},
            'answer_process': False  # ищем только с нужным процессинг статусом
        }
        send_unit = self.conn[config_beauty.bb_db]['templates_sent'].find_one(data)
        if send_unit is None:
            return {'ok': False, 'status': 'template version not find'}

        template_id = send_unit['template_id']
        version = send_unit['version']
        self.conn[config_beauty.bb_db]['templates_stats'].update_one({'id': template_id, 'params.version': version},
                                                                     {'$inc': {'stats.answered': 1}})
        self.conn[config_beauty.bb_db]['templates_sent'].update_one(
            {'template_id': template_id, 'phone': self.phone, 'version': version}, {'$set': {'answer_process': True}})

        return {'ok': True, 'status': 'template version batch update'}

    def check_reply_sendouts(self, channel='wapp'):
        """ Проверяет входящее сообщение не ответ ли на рассылку """

        time_sendouts = int(time.time()) - 86400

        if channel == 'wapp':
            canal = 'chat_api'
        elif channel == 'telegram':
            canal = 'telegram_api'
        else:
            ut.report_exception('No available channel in check_reply_sendouts', r=self.phone)

        data = {
            f'account.{canal}.instanceId': self.instance_id,
            'batch': {'$elemMatch': {'phone': self.phone, 'processing_status': False}},
            '$or': [{'time_start': {'$gte': time_sendouts}}, {'batch.sent_time': {'$gte': time_sendouts}}],
            'sent': True,
        }

        send_unit = self.conn[config_beauty.bb_db]['sendouts'].find_one(data)

        if send_unit is None or 'batch' not in send_unit:
            return {'ok': False, 'status': 'Sendouts not find'}

        sendout_id = send_unit['sendout_id']
        for i in send_unit['batch']:
            if i['phone'] == self.phone and 'processing_status' in i and not i['processing_status']:
                self.conn[config_beauty.bb_db]['sendouts'].update_one(
                    {'sendout_id': sendout_id, 'batch.phone': self.phone}, {
                        '$set': {'batch.$.processing_status': True,
                                 'stats.answered': send_unit['stats']['answered'] + 1}})

        return {'ok': True, 'status': 'Sendouts stats update'}

    def save_phone_for_check_and_warn(self):
        card = {
            'instanceId': self.instance_id,
            'phone': self.phone,
            'Last_msg_time': time.time(),
            'channel': self.message['channel']
        }

        self.conn[config_beauty.bb_db]['clients'].replace_one({'phone': self.phone, 'instanceId': self.instance_id},
                                                              card, upsert=True)
        return {'ok': True, 'status': 'Save phone in clients'}

    def add_phone_in_blacklist(self, token):
        # если добавляют в чс или прислали стоп-слово @@
        if not self.message['from_me'] and '%чс' in self.message['body'].lower() or '@@' in self.message[
            'body'].lower():
            self.conn[config_beauty.bb_db]['bot_clients'].update_many({'accounts.id': self.account['id']},
                                                                      {'$addToSet': {
                                                                          'accounts.$.blacklist': str(self.phone)}})

            for tg in self.account['settings']['notify']:
                msg = '🙅‍♀️ Номер #t{} добавлен в чёрный список'.format(self.phone)
                Bot(token).send_message(tg, msg, reply_markup=config_keyboard.kb)
            return {'ok': True, 'status': f'phone {self.phone} added in blacklist'}

        # Если пользователь прислал "стоп-символ", то добавляем его в ЧС
        stop_symbol = self.account['settings'].get("stop_symbol", "")

        if self.message['from_me'] and stop_symbol != "" and stop_symbol in self.message["body"]:
            self.conn[config_beauty.bb_db]['bot_clients'].update_many({'accounts.id': self.account['id']},
                                                                      {'$addToSet': {
                                                                          'accounts.$.blacklist': str(self.phone)}})

            for tg in self.account['settings']['notify']:
                msg = '🙅‍♀️ Номер #t{} отказался от рассылок.'.format(self.phone)
                Bot(token).send_message(tg, msg, reply_markup=config_keyboard.kb)
            return {'ok': True, 'status': f'phone {self.phone} self added in blacklist'}
        return {'ok': False, 'status': f'No stop symbols in msg text'}

    def check_key_phrase_and_get_reply(self):
        """
        Проверка на наличие ключей во входящем сообщении. Проверяет без учёта регистра
        [{'words': ['test1', 'test2'], 'reply': 'its a reply'}]
        """
        if 'key_phrases' not in self.account or len(self.account['key_phrases']) == 0:
            return {'ok': False, 'status': 'No key phrases'}
        for phrase in self.account['key_phrases']:
            for word in phrase['words']:
                if word.lower() == self.message['body'].lower():
                    ut.send_message_to_queue(self.conn, 'text', self.account, self.account, self.phone, phrase['reply'],
                                             'now')
                    return {'ok': True, 'status': 'Key phrases sent'}
        return {'ok': False, 'status': 'No find key phrases'}


def confirm_or_dicline_rec(conn, flag, client_phone, flag_name, confirm=None):
    # удаляем флаг
    conn[config_beauty.bb_db]['flags'].delete_many({'client_phone': client_phone, 'instanceId': flag['instanceId']})

    account = mongo.Aggregate(conn).get_param_acc_for_id(flag['acc_id'], 'id', 'CRM_data', 'templates', 'settings',
                                                         'telegram_api', 'chat_api')

    for template in account['templates']['timing_messages']:
        if not confirm and template['id'] == flag['message_id'] and 'declined_record' not in template:
            print(debug + ' No declined message')
            return {'ok': True, 'status': 'No declined message'}

    res = sd.confirm_client_recs_for_date(account["CRM_data"], flag['client_id'], flag['date'], confirm=confirm)

    if not res:
        wapp_process_error(
            f'handler_beauty.py read_message_and_check_flags() No recs: {account["CRM_data"]["branch_name"]} {client_phone}')
        return 'No recs'

    if 'No confirm' in res:
        wapp_process_error(f'handler_beauty.py read_message_and_check_flags() confirmation==yes: {res}')
        return 'No confirm'

    send_confirm_msg(conn, res, account, client_phone, flag, flag_name, confirm=confirm)


def send_confirm_msg(conn, res, account, client_phone, flag, flag_name, confirm=None):
    confirmed = False
    declined_text = ''
    reply_text = None
    try:
        if 'attendance' in res:
            if confirm:
                msg = '✅ Запись подтверждена'
                # находим текст ответа
                for template in account['templates']['timing_messages']:
                    if template['id'] == flag['message_id']:
                        reply_text = template[flag_name]

                if reply_text is None:
                    tmp_id = flag['message_id']
                    wapp_process_error(f'No reply text in tmp: {tmp_id}')
                    reply_text = ''

                confirmed = True

            else:
                msg = '❌ Запись отклонена #t{} в филиале {}'.format(client_phone, account['CRM_data']['branch_name'])
                # находим текст ответа
                for template in account['templates']['timing_messages']:
                    if template['id'] == flag['message_id'] and 'declined_record' in template:
                        declined_text = template['declined_record']

        else:

            wapp_process_error(
                'запись не подтверждена для филиала {} {}'.format(account['CRM_data']['branch_name'], str(res)))
            wapp_process_error('flag {}'.format(flag))

            msg0 = '🤷‍♀️ Запись клиента #t{} не подтверждена в филиале 🏙️{}\n\n'.format(client_phone,
                                                                                        account['CRM_data'][
                                                                                            'branch_name'])
            msg = msg0 + '❌ Нет прав на изменение записей для филиала\n\n🏢 {}'.format(
                account['CRM_data']['branch_name'])

        if confirmed:
            if reply_text != '':
                ut.send_message_to_queue(conn, 'text', {'name': account['CRM_data']['branch_name']}, account,
                                         client_phone, reply_text, 'now')
        else:
            if declined_text != '':
                ut.send_message_to_queue(conn, 'text', {'name': account['CRM_data']['branch_name']}, account,
                                         client_phone, declined_text, 'now')

        token = ut.get_tlg_token(conn, account)

        for tg in account['settings']['notify']:
            Bot(token).send_message(tg, msg)


    except:
        ut.report_exception('ошибка подтвержения записи в h_b')
        ut.report_exception(str(traceback.format_exc()))
