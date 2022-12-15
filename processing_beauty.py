import time

import amo
from utilities.green_api import green_to_api
import mongo
import utilities.formating_hooks as form_hook
import utilities.utils as ut
import handler_beauty


def incoming_wapp(r):
    """Входящие хуки от chat api """
    # получаем информацию о первом включении инстанса
    if 'stateInstance' in r:
        amo.notify_sales_about_first_enable_instance(r)
        return 'ok'

    # Маскируем Green-Api под Chat_Api
    if r.get('typeWebhook', '') in ['incomingMessageReceived', 'outgoingMessageReceived', 'outgoingAPIMessageReceived']:
        if r['typeWebhook'] == 'incomingMessageReceived' and r['senderData']['chatId'] == 'status@broadcast' and r['typeWebhook'] == 'outgoingMessageReceived' and r['typeWebhook'] == 'outgoingAPIMessageReceived':
            return {'ok': False, 'status': 'no valid sender'}
        if r['messageData']['typeMessage'] == 'contactMessage':
            return {'ok': False, 'status': 'contact message is not supported'}
        r = green_to_api(r)
    else:
        return {'ok': False, 'status': 'no valid type webhook'}

    if 'messages' in r:
        conn = mongo.get_conn()
        for message in r['messages']:
            standart_message = form_hook.formatting_wapp_hook(message, r['instanceId'])
            handler_beauty.incoming_chatapi_webhook(conn, standart_message, r['instanceId'])
        conn.close()
    return 'ok'


def report_exception(traceback, r=None):
    return ut.report_exception(traceback, r)
