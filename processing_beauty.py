import time

import amo
from utilities.green_api import green_to_api
import mongo
import utilities.formating_hooks as form_hook
import utilities.utils as ut
import handler_beauty


def incoming_wapp(r):
    ts_all = time.time()
    """Входящие хуки от chat api """
    # получаем информацию о первом включении инстанса
    if 'stateInstance' in r:
        amo.notify_sales_about_first_enable_instance(r)
        return 'ok'

    # Маскируем Green-Api под Chat_Api
    if r.get('typeWebhook', '') in ['incomingMessageReceived', 'outgoingMessageReceived', 'outgoingAPIMessageReceived']:
        if r['typeWebhook'] == 'incomingMessageReceived' and r['senderData']['chatId'] == 'status@broadcast':
            return {'ok': False, 'status': 'no valid sender'}
        if r['messageData']['typeMessage'] == 'contactMessage':
            return {'ok': False, 'status': 'contact message is not supported'}
        r = green_to_api(r)
    else:
        return {'ok': False, 'status': 'no valid type webhook'}
    proc_time = 0
    if 'messages' in r:
        ts_proc = time.time()
        with mongo.get_conn() as conn:
            for message in r['messages']:
                standart_message = form_hook.formatting_wapp_hook(message, r['instanceId'])
                handler_beauty.incoming_chatapi_webhook(conn, standart_message, r['instanceId'])
        te_proc = time.time()
        delta_time = round(te_proc - ts_proc, 3)
        proc_time = delta_time
    te_all = time.time()
    delta_time = round(te_all - ts_all, 3)
    all_time = delta_time
    if all_time >= 2:
        print(f'proc: {proc_time} all: {all_time} res: {r}')
    return 'ok'


def report_exception(traceback, r=None):
    return ut.report_exception(traceback, r)
