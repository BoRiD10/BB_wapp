from urllib.parse import quote_plus as quote
from pymongo import MongoClient

from configs import config, config_beauty


def get_conn():
    url = 'mongodb://{user}:{pw}@{hosts}/?replicaSet={rs}&authSource={auth_src}'.format(
        user=quote(config.DB_USER),
        pw=quote(config.DB_PASS),
        rs=config.DB_RS,
        hosts=config.DB_HOSTS,
        auth_src=config.DB_NAME)

    conn = MongoClient(
        url,
        tls=True,
        tlsCAFile=config.CACERT,
    )

    return conn


class Aggregate:
    def __init__(self, conn):
        self.conn = conn

    def get_all_acc_for_instance_id(self, instanceId, *param, channel='wapp', client_name=False, owner_data=False):
        """
        Поиск всех параметров аккаунта по инстансу. Возвращает всех аккаунтов с таким инстансом
        """
        # aggregate_data = [{'$match': {'accounts.chat_api.instanceId': instanceId}},
        #                   {'$unwind': {'path': '$accounts'}},
        #                   {'$match': {'accounts.chat_api.instanceId': instanceId}}]
        #
        # project = {'$project': {'_id': 0}}
        # for i in param:
        #     project['$project'][i] = f'$accounts.{i}'
        #
        # if client_name:
        #     project['$project']['name'] = '$name'
        #
        # if owner_data:
        #     project['$project']['owner'] = '$owner'
        #
        # aggregate_data.append(project)
        # data = list(self.conn['beauty_bot']['bot_clients'].aggregate(aggregate_data))

        project = {
            '_id': 0,
        }
        for i in param:
            project[f'accounts.{i}'] = 1

        if client_name:
            project[f'name'] = 1

        if owner_data:
            project['owner'] = 1

        bot_clients = list(self.conn['beauty_bot']['bot_clients'].find({'accounts.chat_api.instanceId': instanceId}, project))
        accounts = [[bc['name']] + [bc['owner']] + bc['accounts'] for bc in bot_clients]
        data = [dict({'name': account[0], 'owner': account[1]}, **acc) for account in accounts for acc in account[2:]]

        if len(data) > 0:
            return data
        else:
            return False

    # Поиск параметров аккаунта по id аккаунта
    def get_param_acc_for_id(self, acc_id, *param, client_name=False, owner=False, active_acc=False, container=False):
        aggregate_data = [{'$match': {'accounts.id': acc_id}}, {'$unwind': {'path': '$accounts'}},
                          {'$match': {'accounts.id': acc_id}}]
        project = {'$project': {'_id': 0}}
        for i in param:
            project['$project'][i] = f'$accounts.{i}'

        if client_name:
            project['$project']['name'] = '$name'

        if owner:
            project['$project']['owner'] = '$owner'

        if active_acc:
            project['$project']['active_account'] = '$active_account'

        if container:
            project['$project']['container'] = '$container'

        aggregate_data.append(project)
        setting = list(self.conn[config_beauty.bb_db]['bot_clients'].aggregate(aggregate_data))
        if len(setting) != 0:
            return setting[0]
        else:
            return False
