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
