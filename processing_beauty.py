import time

import amo
from utilities.green_api import green_to_api
import mongo
import utilities.formating_hooks as form_hook
import utilities.utils as ut
import handler_beauty
from wapp_logic import Adapter


def incoming_wapp(r):
    """Входящие хуки от chat api """
    # получаем информацию о первом включении инстанса
    if 'stateInstance' in r or r.get('messages', [{'wh_type': 'nan'}])[0]['wh_type'] == 'authorization_status':
        # если хук не от green api, маскируем его под wappi
        if 'stateInstance' not in r:
            r = Adapter.FormatHook().wappi_to_green_auth(r)
        if 'error' not in r:
            amo.notify_sales_about_first_enable_instance(r)
            return 'ok'
    # Маскируем Green-Api под Chat_Api
    if 'typeWebhook' in r and r['typeWebhook'] in ['incomingMessageReceived', 'outgoingMessageReceived',
                                                   'outgoingAPIMessageReceived']:
        if r['typeWebhook'] == 'incomingMessageReceived' and r['senderData']['chatId'] == 'status@broadcast':
            return {'ok': False, 'status': 'no valid sender'}
        if r['messageData']['typeMessage'] == 'contactMessage':
            return {'ok': False, 'status': 'contact message is not supported'}
        r = green_to_api(r)
        if 'messages' in r:
            message = r['messages'][0]
            standart = form_hook.formatting_wapp_hook(message, r['instanceId'])
    elif 'messages' in r and type(r['messages']) is list and len(r['messages']) != 0 and 'body' in r['messages'][0]:
        standart = Adapter.FormatHook().wappi_to_standart(r)
    else:
        return {'ok': False, 'status': 'no valid type webhook'}
    conn = mongo.get_conn()
    handler_beauty.incoming_chatapi_webhook(conn, standart, standart['id'])
    conn.close()

    return 'ok'


def report_exception(traceback, r=None):
    return ut.report_exception(traceback, r)
