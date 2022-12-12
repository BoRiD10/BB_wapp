from loguru import logger

from configs import config
from exceptions.except_config import users_errors, system_errors, regular_errors
from telegram import Bot


class CustomException(BaseException):
    def __init__(self, exc_id: str, user_id: int, log_path='botsarmy/logs/exceptions/custom_error.log') -> None:
        self.exc_id = exc_id
        self.user_id = user_id
        self.log_path = log_path

    def send_message(self, *args):
        """Отправляет сообщение с описанием ошибки в тг"""
        msg = users_errors[self.exc_id]
        if len(args) > 0:
            if len(args) == 1:
                msg = msg % args[0]
            else:
                msg = msg % args
        Bot(config.beauty_whatsapp_bot_token).send_message(self.user_id, msg)

    def log_error(self, *args):
        """Логирует системные ошибки"""
        msg = system_errors[self.exc_id]
        if len(args) > 0:
            if len(args) == 1:
                msg = msg % args[0]
            else:
                msg = msg % args
        logger.remove()
        logger.add(self.log_path, format='{time} {level} {message}',
                   level='INFO', rotation='00:00', compression='tar.xz')
        logger.error(msg)

    def chose_action(self, *args):
        """По id ошибки выбирает, что нужно сделать"""
        if self.exc_id in users_errors:
            self.send_message(args)
        if self.exc_id in system_errors:
            self.log_error(args)
        if self.exc_id in regular_errors:
            self.send_msg_for_regular_tasks(args)

    def send_msg_for_regular_tasks(self, *args):
        """
        Отправляет сообщение в группу
        при ошибках в регулярных тасках.
        """
        tb = args[0][0]
        if len(tb) > 3500:
            tb = tb[:3500]
        traceback_msg = '```\n' + tb + '\n```'
        msg = regular_errors[self.exc_id] % traceback_msg

        Bot(config.bb_dev_bot_token).send_message(self.user_id, msg)
