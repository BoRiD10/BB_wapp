# -*- coding: utf-8 -*-
import re
import time

import pytz

import mongo
import review
import utilities.utils as ut
from utilities.wapp_process import WappHooksProcess
from configs import config_beauty, text_templates

moscow = pytz.timezone('Europe/Moscow')


def incoming_chatapi_webhook(conn, message, instance_id):
    """Функция обработки входящего хука сообщения от chat_api"""
    if '#otziv' in message['body'] and text_templates.create_review_group[:20] not in message['body']:
        change_rev_group(conn, message, instance_id)
        return 'switch group'
    ts_acc = time.time()
    accounts = mongo.Aggregate(conn).get_all_acc_for_instance_id(instance_id, 'settings', 'ignore_list', 'chat_api',
                                                                 'id', 'trello', 'CRM_data', 'key_phrases',
                                                                 client_name=True, owner_data=True)
    te_acc = time.time()
    delta_time = round(te_acc - ts_acc, 3)
    acc_time = delta_time
    if not accounts:
        print(f'Account not found: {instance_id}')
        return {'ok': False, 'status': f'Account not found'}

    phone = ut.get_digits_from_string(message['phone'])
    for account in accounts:
        if not ut.account_paid(account):
            continue
        # Получем токен для поддержки партнерских ботов
        ts_token = time.time()
        token = ut.get_tlg_token(conn, account)
        te_token = time.time()
        delta_time = round(te_token - ts_token, 3)
        token_time = delta_time

        # Получение списка номеров исключений(которые не надо проверять)
        reply_accept = account['settings']['reply_msg_check']
        ignore_list = account['ignore_list']
        process_wapp = WappHooksProcess(conn, account, message, phone, instance_id)

        # Отправляем трансляцию в тг
        ts_translate = time.time()
        process_wapp.send_translation_message()
        te_translate = time.time()
        delta_time = round(te_translate - ts_translate, 3)
        translate_time = delta_time

        # Проверка не ответ ли это на рассылку или шаблон
        if not message['from_me']:

            # проверяет на наличие ключевых слов в сообщении
            process_wapp.check_key_phrase_and_get_reply()

            # Сохраняем номер в базу для трансфера в базу ycl
            ts_save = time.time()
            process_wapp.save_phones_in_db()
            te_save = time.time()
            delta_time = round(te_save - ts_save, 3)
            save_time = delta_time

            if message['type'] in ['chat', 'buttons_response']:
                text = message['body']
            else:
                text = message['caption']
            debug = f'acc: {acc_time} len:{len(accounts)} inst: {instance_id} token: {token_time} translate: {translate_time} save: {save_time}'
            if text is not None:
                # Проверяем, сообщение для подтверждения
                ts_confirm = time.time()
                confirm_status = process_wapp.read_message_and_check_flags(text)
                te_confirm = time.time()
                delta_time = round(te_confirm - ts_confirm, 3)
                confirm_time = delta_time
                debug += f' confirm: {confirm_time}'
                if confirm_status.get('ok', False):
                    print(debug)
                    return {'ok': True, 'status': 'Confirm message processed'}
                # Проверяем, сообщение ответ на отзыв
                ts_rev = time.time()
                review_status = review.check_review(conn, text, phone, account['id'])
                te_rex = time.time()
                delta_time = round(te_rex - ts_rev, 3)
                rev_time = delta_time
                debug += f' rev: {rev_time}'
                if review_status.get('ok', False):
                    print(debug)
                    return {'ok': True, 'status': 'Review message processed'}
            # Проверяем, сообщение ответ на рассылку
            ts_sendout = time.time()
            process_wapp.check_reply_sendouts(channel=message['channel'])
            te_sendout = time.time()
            delta_time = round(te_sendout - ts_sendout, 3)
            sendout_time = delta_time
            # Проверяем, сообщение ответ на сообщение для потеряшек
            ts_template = time.time()
            process_wapp.check_reply_tmp()
            te_template = time.time()
            delta_time = round(te_template - ts_template, 3)
            template_time = delta_time

            ts_heck = time.time()
            # Проверка на нахождение номера в списке исключения, если нет, то обрабатываем
            if phone not in ignore_list and reply_accept == 1 and len(phone) in range(10, 13):
                process_wapp.save_phone_for_check_and_warn()
            te_heck = time.time()
            delta_time = round(te_heck - ts_heck, 3)
            heck_time = delta_time
            debug += f' sendout: {sendout_time} template: {template_time} heck: {heck_time}'
            print(debug)

        process_wapp.add_phone_in_blacklist(token)

    return {'accounts': accounts}


def change_rev_group(conn, message, instance_id):
    # Изменение трансляции отзывов в существующую группу в WA
    tag = re.findall(r'(#\w+)', message['body'])[0]
    branch_id = tag[6:]
    group_id = message['chatId']  # !
    accounts = mongo.Aggregate(conn).get_all_acc_for_instance_id(instance_id, 'chat_api', 'settings', 'CRM_data',
                                                                 channel=message['channel'], client_name=True)
    if accounts:
        acc = accounts[0]
    else:
        ut.report_exception('switch rev group error')
        ut.report_exception(str(message))
        return 'Error'

    if 'review_messages' in acc:
        try:
            conn[config_beauty.bb_db]['bot_clients'].update_one(
                {'accounts.CRM_data.branch': branch_id, 'accounts.chat_api.instanceId': instance_id},
                {'$set': {'accounts.$.review_messages.0.WA_alerts.0': group_id}})
            success_text = text_templates.default_review_messages['add_WA_group'].format(branch_id)
            ut.send_message_to_queue(conn, 'text', acc, acc, group_id, success_text, 'urgent')

        except:
            err_text = text_templates.default_review_messages['no_branch_group'].format(branch_id)
            ut.send_message_to_queue(conn, 'text', {'name': 'msg_to_group'}, acc, group_id, err_text, 'urgent')
    else:
        err_text = f'Не подключена цепочка отзывов проверьте в настройках щаблонов'
        ut.send_message_to_queue(conn, 'text', {'name': 'msg_to_group'}, acc, group_id, err_text, 'urgent')
