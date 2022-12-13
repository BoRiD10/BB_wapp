from loguru import logger

import utilities.utils as ut


def formatting_info(text):
    logger.remove()
    logger.add('BB_wapp/logs/utilities/formatting_info.log', format='{time} {level} {message}',
               level='INFO', rotation='00:00', compression='zip')
    logger.info(text)


def formatting_wapp_hook(chat_api_hook, instance_id):
    inst_id = instance_id
    from_me = chat_api_hook['fromMe']
    datetime = chat_api_hook['time']
    chat_id = ut.get_digits_from_string(chat_api_hook['chatId'])
    phone = ut.get_digits_from_string(chat_api_hook['chatId'], ['@', '-'])
    sender_name = chat_api_hook['senderName']
    msg_type = chat_api_hook['type']
    text = chat_api_hook['body']
    is_forwarded = chat_api_hook['isForwarded']
    message_id = chat_api_hook['id']
    if chat_api_hook['type'] in ['chat', 'buttons_response']:
        data = standard_message(text, inst_id, from_me, is_forwarded, datetime, chat_id, phone, sender_name,
                                message_id, msg_type, channel='wapp')
        return data
    else:
        caption = chat_api_hook['caption']
        if caption is None:
            caption = ''
        data = standard_message(text, inst_id, from_me, is_forwarded, datetime, chat_id, phone, sender_name,
                                message_id, msg_type, caption=caption, channel='wapp')
        return data


def formatting_tg_hook(tg_hook):
    formatting_info(str(tg_hook))
    inst_id = str(tg_hook['meta']['instance']['id'])
    from_me = tg_hook['fromMe']
    datetime = tg_hook['date']
    chat_id = str(tg_hook['chat']['id'])
    sender_name = tg_hook['from_user']['username']
    text = 'chat'
    caption = None
    cached = False
    message_id = tg_hook['message_id']

    if 'phone_number' in tg_hook['from_user'] and tg_hook['from_user']['phone_number'] is not None and '*' not in \
            tg_hook['from_user']['phone_number']:
        phone = str(tg_hook['from_user']['phone_number'])
    else:
        phone = 'N/A'

    msg_type = 'chat'
    if 'media_url' in tg_hook and tg_hook['media_url'] is not None:
        if 'text' in tg_hook:
            caption = tg_hook['text']
        if 'photo' in tg_hook and tg_hook['photo'] is not None:
            msg_type = 'photo'
            text = tg_hook['media_url']
        elif 'video' in tg_hook and tg_hook['video'] is not None:
            msg_type = 'video'
            text = tg_hook['media_url']
        elif 'voice' in tg_hook and tg_hook['voice'] is not None:
            msg_type = 'voice'
            text = tg_hook['media_url']
        elif 'document' in tg_hook and tg_hook['document'] is not None:
            msg_type = 'document'
            text = tg_hook['media_url']
        elif 'venue' in tg_hook and tg_hook['venue'] is not None:
            msg_type = 'venue'
            text = tg_hook['media_url']
    else:
        msg_type = 'chat'
        text = tg_hook['text']

    if 'forward_from' in tg_hook and tg_hook['forward_from'] is not None:
        is_forwarded = 1
    else:
        is_forwarded = 0

    data = standard_message(text, inst_id, from_me, is_forwarded, datetime, chat_id, phone, sender_name, message_id,
                            msg_type=msg_type, caption=caption, channel='telegram', cached=cached)

    return data


def standard_message(text, inst_id, from_me, is_forwarded, datetime, chat_id, phone, sender_name, message_id,
                     msg_type='chat', caption=None, channel='wapp', cached=False):
    data = {
        'body': text,
        'id': inst_id,
        'from_me': from_me,
        'is_forwarded': is_forwarded,
        'time': datetime,
        'chat_id': chat_id,
        'phone': phone,
        'type': msg_type,
        'sender_name': sender_name,
        'channel': channel,
        'message_id': message_id,
        'cached': cached
    }

    if caption is not None:
        data['caption'] = caption

    return data
