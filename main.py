import traceback

from flask import Flask, request
import processing_beauty


app = Flask(__name__)


# Обработчик для всех входящих вебхуков chat_api для Бьюти Бота
@app.route('/beauty_wapp', methods=['GET', 'POST'])
def beauty_wapp():
    r = request.get_json()

    try:
        processing_beauty.incoming_wapp(r)
    except:
        processing_beauty.report_exception(traceback.format_exc(), r)

    return 'ok'

if __name__ == "__main__":

    r = {
        "typeWebhook": "incomingMessageReceived",
        "instanceData": {
            "idInstance": 5511746468111,
            "wid": "79167848284@c.us",
            "typeInstance": "whatsapp"
        },
        "timestamp": 1662241489,
        "idMessage": "3AE43BCD2BBF3F974D30",
        "senderData": {
            "chatId": "79167848284@c.us",
            "sender": "79167848284@c.us",
            "senderName": "Наталия"
        },
        "messageData": {
            "typeMessage": "textMessage",
            "textMessageData": {
                "textMessage": "Ключ"
            }
        }
    }
    try:
        processing_beauty.incoming_wapp(r)
    except:
        processing_beauty.report_exception(traceback.format_exc(), r)