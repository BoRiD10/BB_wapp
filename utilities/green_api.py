import requests
from loguru import logger


def incoming_hooks_info(text):
    logger.remove()
    logger.add('botsarmy/logs/green_api/incoming_hooks.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def outgoing_hooks_info(text):
    logger.remove()
    logger.add('botsarmy/logs/green_api/outgoing_hooks.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='tar.xz')
    logger.info(text)


def green_to_api(green_msg):
    """ Перевод хука Green_API к виду chat_API"""
    if green_msg['typeWebhook'] == 'outgoingMessageReceived':
        # outgoing_hooks_info(green_msg)
        fromMe = True
    elif green_msg['typeWebhook'] == 'outgoingAPIMessageReceived':
        # outgoing_hooks_info(green_msg)
        fromMe = True
    else:
        # incoming_hooks_info(green_msg)
        fromMe = False

    if green_msg['messageData']['typeMessage'] == 'textMessage':
        type_msg = 'chat'
        msg = green_msg['messageData']['textMessageData']['textMessage']
        caption = ''

    elif green_msg['messageData']['typeMessage'] == 'buttonsResponseMessage':
        type_msg = 'chat'
        msg = green_msg['messageData']['buttonsResponseMessage']['selectedButtonText']
        caption = ''

    elif green_msg['messageData']['typeMessage'] == 'extendedTextMessage':
        type_msg = 'chat'
        msg = green_msg['messageData']['extendedTextMessageData']['text']
        caption = ''

    elif green_msg['messageData']['typeMessage'] == 'locationMessage':
        type_msg = 'venue'
        msg = str(green_msg['messageData']['locationMessageData']['latitude']) + ';' + str(
            green_msg['messageData']['locationMessageData']['latitude'])
        caption = ''

    elif green_msg['messageData']['typeMessage'] == 'imageMessage':
        type_msg = 'photo'
        msg, caption = create_msg_caption(green_msg)

    elif green_msg['messageData']['typeMessage'] == 'videoMessage':
        type_msg = 'video'
        msg, caption = create_msg_caption(green_msg)

    elif green_msg['messageData']['typeMessage'] == 'audioMessage':
        type_msg = 'voice'
        msg, caption = create_msg_caption(green_msg)

    elif green_msg['messageData']['typeMessage'] == 'documentMessage':
        type_msg = 'document'
        msg, caption = create_msg_caption(green_msg)

    elif green_msg['messageData']['typeMessage'] == 'quotedMessage':
        type_msg = 'chat'
        msg = green_msg['messageData']['extendedTextMessageData']['text']
        caption = ''
    else:
        type_msg = 'chat'
        msg = ''
        caption = ''

    isForwarded = 0

    if green_msg['senderData'].get('sender', '1') == green_msg['senderData']['chatId']:
        self = 1
    else:
        self = 0

    chat_msg = {'messages': [
        {'body': msg,
         'fromMe': fromMe,
         'self': self,
         'isForwarded': isForwarded,
         'author': '',
         'time': green_msg['timestamp'],
         'chatId': green_msg['senderData']['chatId'],
         'messageNumber': 0,
         'type': type_msg,
         'senderName': green_msg['senderData']['senderName'],
         'caption': caption,
         'quotedMsgBody': 'None',
         'quotedMsgId': 'None',
         'quotedMsgType': 'None',
         'chatName': green_msg['senderData']['senderName'],
         'id': green_msg['idMessage']
         }],
        'instanceId': str(green_msg['instanceData']['idInstance'])
    }
    return chat_msg


'''Обратный хук при отправке через TLGRM'''


def return_hook(message):
    params = {'body': message['body'],
              'fromMe': True,
              'time': message['time'],
              'chatId': message['phone'] + '@c.us',
              'messageNumber': 0,
              'type': message['type'],
              'senderName': message['bot_client'],
              'quotedMsgBody': 'None',
              'quotedMsgId': 'None',
              'quotedMsgType': 'None',
              'chatName': message['bot_client']
              }

    if 'caption' in message:
        params.update({'caption': message['caption']})

    chat_msg = {'messages': [params], 'instanceId': message['wapp']['instanceId']}
    return requests.post(url='https://www.botsarmy.biz/green_api', json=chat_msg)


'''Доп функция'''


def create_msg_caption(green_msg):
    msg = green_msg['messageData']['fileMessageData']['downloadUrl']
    if 'caption' in green_msg['messageData']['fileMessageData']:
        caption = green_msg['messageData']['fileMessageData']['caption']
    else:
        caption = ''
    return msg, caption


'''Тесты'''
# print(green_api_instance('f2ad32bf51d7e646c0e36a13e66bc06fad8152694336f13517').createInstance().json())
# print(green_api_instance('f2ad32bf51d7e646c0e36a13e66bc06fad8152694336f13517').getInstances().json())
# print(Sending('74d080e6f5c2f886b293a4f4ef25c648a3916c86275863f756').send_msg(7867, '79154474072@c.us', 'Try').text)
# print('data:image/png;base64,' + settings_green_api('7867', '74d080e6f5c2f886b293a4f4ef25c648a3916c86275863f756').get_qr().json()['message'])
# print(settings_green_api('74d080e6f5c2f886b293a4f4ef25c648a3916c86275863f756').get_state_snstance(7867).json())
# Sending('7867', '74d080e6f5c2f886b293a4f4ef25c648a3916c86275863f756').send_location('79167848284', 55.88347115024764, 37.48961268094533, '')

# print(Sending('74d080e6f5c2f886b293a4f4ef25c648a3916c86275863f756').send_Down_File(7867, '79167848284@c.us', 'https://api.green-api.com/waInstance7867/downloadFile/eyJ0eXBlIjoidmlkZW9NZXNzYWdlIiwiZG93bmxvYWRVcmwiOiJodHRwczovL21tZy53aGF0c2FwcC5uZXQvZC9mL0FoaFh5VEx4d0NXNDZjZWtwY2R2SVEybURqN2liZ1otcjRMQXR1dTFNY0kwLmVuYyIsImRpcmVjdFBhdGgiOiIvdi90NjIuNzE2MS0yNC80MDgzMjQ2MV8yMTU2ODY3NTMyODI1MTRfMzUzMjM4Mzk2NjEwMTk1MDQwMV9uLmVuYz9jY2I9MTEtNCZvaD1jMTA4OTc3YmQyNjE1MDc1M2JmMGViOGRkMmY2NmI5OCZvZT02MEFFNzEzMiIsIm1lZGlhS2V5IjoiSFcvVXBpMHhCTGZuckZFbkNXbGxWTitkT0w5djhQa0ZqZWwxTHBiU2w3Yz0iLCJtaW1lVHlwZSI6InZpZGVvL21wNCIsImZpbGVMZW5ndGgiOjU1ODIyNTd9', caption = 'yes').text)
