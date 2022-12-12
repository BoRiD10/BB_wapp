import re
import traceback

import emoji

import mongo
import utilities.search_data as sd
import utilities.utils as ut
from configs import config_beauty, text_templates


def check_review(conn, text, phone, acc_id):
    client = list(
        conn[config_beauty.bb_db]['clients_review'].find({'phone': phone, 'acc_id': acc_id}).sort('_id', -1).limit(1))

    if len(client) == 0:
        return {'ok': False, 'status': 'No review state'}

    client = client[0]
    records = None
    send_buttons = False
    # review_status = 'send rev'
    WA_alerts_list = client['WA_alerts']
    current_text = client['prev_text']
    status = client['status']
    type_msg = client['format']
    fail_counter = client['fail_counter']
    next_step_text = ''
    account = mongo.Aggregate(conn).get_param_acc_for_id(acc_id, 'id', 'review_messages', 'chat_api', 'telegram_api',
                                                         'CRM_data', 'settings', client_name=True, owner=True)
    branch_id = account['CRM_data']['branch']
    if 'template_id' in client:
        template_id = client['template_id']
    else:
        if type(account['review_messages'][0]) is dict:
            template_id = account['review_messages'][0]['id']
        if type(account['review_messages'][0]) is list:
            template_id = account['review_messages'][0][0]['id']

    if type(account['review_messages'][0]) is dict:
        rev_messages = account['review_messages']
    if type(account['review_messages'][0]) is list:
        for tmp in account['review_messages']:
            if tmp[0]['id'] == template_id:
                rev_messages = tmp

    message = rev_messages[status]

    # Обработка оценки
    if type_msg == 'est':
        est, estimate = get_est_from_text(text, acc_id, buttons=send_buttons)
        if est != 'est not found':
            fail_counter = 0
        else:
            send_admins(conn, account, phone, text)
            fail_counter = fail_counter + 1
            if fail_counter == 3:
                conn[config_beauty.bb_db]['clients_review'].delete_many({'phone': phone, 'acc_id': acc_id})
            else:
                conn[config_beauty.bb_db]['clients_review'].update_one(
                    {'phone': phone, 'acc_id': acc_id, 'records_id': client['records_id']},
                    {'$set': {'fail_counter': fail_counter}})
            return {'ok': False, 'status': 'Estimate not find'}

        if estimate < message['valid']:
            good_estimate = 0
            text = form_negative_message(conn, client, phone, current_text, est, branch_id)
            send_admins(conn, account, phone, text)
            for user in WA_alerts_list:
                ut.send_message_to_queue(conn, 'text', account, account, user, text, 'now')

        if estimate <= 2:
            # ! Отправка овнеру
            good_estimate = 0
            text = form_negative_message(conn, client, phone, current_text, est, branch_id)
            ut.send_tmsg_to_queue(conn, account, account['owner']['telegram_id'], text, 'now')

        if estimate >= message['valid']:
            good_estimate = 1

        for i in range(status + 1, len(rev_messages)):
            if rev_messages[i]['active']:
                type_msg = rev_messages[i]['format']
                status = i - status
                next_step_text = rev_messages[i]['body']
                break

        if next_step_text == '':
            return {'ok': True, 'status': 'No second step'}

    if type_msg == 'wait_comment':
        if isinstance(client['records_id'], list):
            records = list(conn[config_beauty.bb_db]['records'].find(
                {'company_id': int(branch_id), '$or': [{'resource_id': ids} for ids in client['records_id']]}))
            records = records[0]
        else:
            records = conn[config_beauty.bb_db]['records'].find_one({'company_id': int(branch_id), 'resource_id': int(client['records_id'])})
        if 'success_visits_count' in records['data']['client']:
            success_visits = str(records['data']['client']['success_visits_count'])
        else:
            success_visits = 'Не определено'
        client_name = records['data']['client']['name']
        text = text_templates.review_messages['fail_rev'] % (client_name, phone, success_visits, text)
        ut.send_tmsg_to_queue(conn, account, account['owner']['telegram_id'], text, 'now')
        send_admins(conn, account, phone, text)
        for user in WA_alerts_list:
            ut.send_message_to_queue(conn, 'text', account, account, user, text, 'now')
        conn[config_beauty.bb_db]['clients_review'].delete_many({'phone': phone, 'acc_id': acc_id})
        return {'ok': True, 'status': 'Received Wait message'}

    # Отправка ссылок на отзыв в конце, если норм оценки
    if type_msg == 'text':
        num_steps = 0
        for i in rev_messages:
            if i['format'] == 'est' and i['active']:
                num_steps += 1

        if num_steps <= client['review'] + good_estimate:
            conn[config_beauty.bb_db]['clients_review'].delete_many({'phone': phone, 'acc_id': acc_id})
        else:
            next_step_text = rev_messages[-1]['fail_text']
            type_msg = 'wait_comment'

    if len(re.findall(r'{(.+?)}', next_step_text)) != 0:
        multiple_recs = None
        if records is None:
            if isinstance(client['records_id'], list):
                records = list(conn[config_beauty.bb_db]['records'].find(
                    {'company_id': int(branch_id), '$or': [{'resource_id': ids} for ids in client['records_id']]}))
                recs = []
                for record in records:
                    dat = record['data']
                    dat.update({'name': record['name']})
                    recs.append(dat)
                multiple_recs = recs
                records = records[0] if len(records) != 0 else None
            else:
                records = conn[config_beauty.bb_db]['records'].find_one(
                    {'company_id': int(branch_id), 'resource_id': int(client['records_id'])})
        if records is None:
            for user in WA_alerts_list:
                text = text_templates.review_messages['none_record'] % phone
                ut.send_message_to_queue(conn, 'text', account, account, user, text, 'now')
                conn[config_beauty.bb_db]['clients_review'].delete_many({'phone': phone, 'acc_id': acc_id})
                return {'ok': True, 'status': 'Not find record data'}

        keys = sd.get_record_keys(account, records, multiple_recs=multiple_recs, message=next_step_text, conn=conn)
        next_step_text = ut.insert_keys_into_templates(keys, next_step_text)

    # Логика сообщения, на которое нужно ответить
    if type_msg in ['est', 'wait_comment']:
        if type_msg == 'est':
            next_step_text = next_step_text + get_rev_text(acc_id)
            ut.send_message_to_queue(conn, 'text', account, account, phone, next_step_text, 'now')
            processed_status = {'ok': True, 'status': 'Next estimate step send'}
        else:
            ut.send_message_to_queue(conn, 'text', account, account, phone, next_step_text, 'now')
            processed_status = {'ok': True, 'status': 'Wait messages send'}
        conn[config_beauty.bb_db]['clients_review'].update_one(
            {'phone': phone, 'acc_id': acc_id, 'records_id': client['records_id']},
            {'$inc': {'status': status, 'review': good_estimate},
             '$set': {'format': type_msg, 'fail_counter': fail_counter, 'prev_text': next_step_text}})
        return processed_status

    if type_msg == 'text':
        ut.send_message_to_queue(conn, 'text', account, account, phone, next_step_text, 'now')
        return {'ok': True, 'status': 'All review messages send'}


def get_est_from_text(text, acc_id, buttons=False):
    text_est = text_templates.text_est_2
    for locale in config_beauty.locale:
        if acc_id in locale['acc_id']:
            text_est = locale.get('text_est_2', text_templates.text_est_2)

    if buttons:
        est = ' '.join(text.split(' ')[1:])
        if est in list(text_templates.text_est.keys()):
            estimate = text_templates.text_est[est]
        else:
            return 'est not found', None
    else:
        for est in list(text_est.keys())[::-1]:
            text_list = [e for e in text.lower() if e in emoji.UNICODE_EMOJI['en']]
            text_clean = re.sub(r'[^\w\s]', ' ', text)
            text_list += [letter for letter in text_clean.lower().split(' ') if letter != '' and letter != '-']
            est_list = est.replace(' -', '').lower().split(' ')
            est_text = ' '.join(est_list[2:])
            est_list = est_list[:2] + [est_text]
            check_text = [True if word in est_list or est_text in text_clean else False for word in text_list]
            check_text = True if True in check_text else False
            if check_text:
                estimate = text_est[est]
                break
            else:
                estimate = None

        if estimate is None:
            return 'est not found', None

    return est, estimate


def form_negative_message(conn, client, phone, current_text, est, branch_id):
    if isinstance(client['records_id'], list):
        records = list(conn[config_beauty.bb_db]['records'].find({'company_id': int(branch_id), '$or': [{'resource_id': ids} for ids in client['records_id']]}))
        cl = records[-1]['data']['client']
    else:
        records = conn[config_beauty.bb_db]['records'].find_one({'company_id': int(branch_id), 'resource_id': int(client['records_id'])})
        cl = records['data']['client']

    if 'success_visits_count' in cl:
        success_visits = str(cl['success_visits_count'])
    else:
        success_visits = 'Не определено'

    client_name = cl['name']
    text = text_templates.review_messages['bad_est'] % (client_name, phone, success_visits, current_text, est)
    return text


def get_rev_text(acc_id):
    rev_text = text_templates.rev_extra_text
    for locale in config_beauty.locale:
        if acc_id in locale['acc_id']:
            rev_text = locale.get('rev_extra_text', text_templates.rev_extra_text)
    return rev_text


def send_admins(conn, account, phone, text):
    # Логика "я вас не понял"
    all_admins = [int(user) for users in account['settings']['admins'] for user in users if 'tlg_review' in users[user]]
    all_admins = set(all_admins)
    for user in all_admins:
        admin_text = text_templates.review_messages['admin_warn'] % phone
        try:
            ut.send_tmsg_to_queue(conn, account, int(user), admin_text, 'now')
        except:
            ut.report_exception('ошибка отправки сообщения админам в review, строка 34')
            ut.report_exception(str(traceback.format_exc()), text)