import traceback

from loguru import logger

import mongo
from configs import config_beauty, config

from exceptions.custom_exception import CustomException
from telegram import Bot
import utilities.utils as ut
from wapp import GreenApi
from wapp_logic import target


def inst_state_log(text):
    logger.remove()
    logger.add('BB_wapp/logs/state_instance/state_instance_info.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


class Triggers:

    def __init__(self):
        self.url = 'https://tglk.ru/'

    def bot_client_created(self, branch_id):
        url = self.url + 'in/lqOv7fP9BsxvrKyY'
        params = {
            'branch_id': branch_id
        }
        r = ut.get_session().post(url=url, json=params)
        if r.status_code != 200 or not r.json()['status']:
            raise ValueError(f'Ответ из триггеров с ошибкой: {r.status_code}\n\n{params}\n\n{r.text}')
        return {'ok': True}


def notify_sales_about_first_enable_instance(r):
    if r['stateInstance'] == 'authorized':
        conn = mongo.get_conn()
        instance_id = str(r['instanceData']['idInstance'])
        account = mongo.Aggregate(conn).get_all_acc_for_instance_id(instance_id, 'chat_api', 'CRM_data', owner_data=True)
        conn.close()
        try:
            Triggers().bot_client_created(account[0]["CRM_data"]["branch"])
        except:
            tb = traceback.format_exc(chain=False)
            exception = CustomException('amo_1', config_beauty.tg_err_group_id)
            exception.chose_action(tb)
        try:
            resp = target.Wapp(account[0]['chat_api']).set_settings(state=True)
            if resp['saveSettings']:
                msg = f'Хуки о состоянии отключены для филиала {account[0]["CRM_data"]["branch"]}'
                inst_state_log(msg)
        except:
            tb = traceback.format_exc(chain=False)
            msg = f'{account[0]["CRM_data"]["branch_name"]}({account[0]["CRM_data"]["branch"]})\n\n'
            msg += '```\n' + tb + '\n```'
            exception = CustomException('amo_2', config_beauty.tg_err_group_id)
            exception.chose_action(msg)
