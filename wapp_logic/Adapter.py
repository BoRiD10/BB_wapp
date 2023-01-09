import base64
from wapp_logic.models import ClearData


class GreenApi:

    def set_settings(self, first_data):
        clear_data = ClearData.clear_set_settings(first_data)
        return clear_data


class Wappi:

    def set_settings(self, first_data):
        data = {'saveSettings': first_data}
        clear_data = ClearData.clear_set_settings(data)
        return clear_data


class FormatHook:

    def wappi_to_green_auth(self, first_data):
        instance = first_data['messages'][0].get('profile_id', None)
        if instance is None:
            return {'error': 'Instance id not in hook'}
        status = 'authorized' if first_data['messages'][0].get('status', 'offline') == 'online' else 'notAuthorized'
        data = {
            "instanceData": {
                "idInstance": instance
            },
            "stateInstance": status
        }
        clear_data = ClearData.clear_wappi_auth_hook(data)
        return clear_data

    def wappi_to_standart(self, r):
        message = r['messages'][0]
        from_me = True if message['wh_type'] != 'incoming_message' else False
        data = {
            'body': message['body'],
            'id': message['profile_id'],
            'from_me': from_me,
            'is_forwarded': False,
            'time': message['time'],
            'chat_id': message['chatId'],
            'phone': message['from'],
            'type': message['type'],
            'sender_name': message['senderName'],
            'channel': 'wapp',
            'message_id': message['id'],
            'cached': False
        }
        if 'caption' in message:
            data['caption'] = message['caption']
            # if data['type'] == 'image':
            #     file = base64.b64decode(message['body'])
            #     photo = io.BytesIO(file)
            #     name = f'{message["id"]}.jpg'
            #     path = config_beauty.static_path + name
            #     with open(path, 'wb') as out:
            #         out.write(photo.read())
            #     link = s3_save().upload_file_from_static(name)
            #     data['body'] = str(link)
            #     os.remove(path)
        clear_data = ClearData.clear_standart_hook(data)
        return clear_data


class FormatData(GreenApi, Wappi):

    def __init__(self, chat_api_data):
        self.chat_api_data = chat_api_data
        if self.chat_api_data['url'] in ['green-api', 'https://green-api/']:
            self.wapp_api = GreenApi
        if self.chat_api_data['url'] in ['wappi']:
            self.wapp_api = Wappi

    def choose_adapt_class(self):
        return self.wapp_api()
