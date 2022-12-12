users_errors = {
    'payments_1': 'Не удалось получить количество сотрудников на филиале %s.\n\n Данная ошибка может возникать в случае окончания лецензии CRM системы или отсутствие прав у бота.',
    'payments_2': 'Не удалось сгенерировать ссылки на оплату!\n\nОбратитесь в поддержку.',
    'payments_3': 'Не удалось сохранить информацию об автоплатеже!\n\nОбратитесь в поддержку.',
    'autopay_1': ('🔥 Ой! %s автоплатеж за Бьюти Бота, а у нас не получилось посчитать Ваш тариф...'
                  '\n\n*Причина*:\nНе удалось получить количество сотрудников на филиале *%s*.'
                  '\n\n Данная ошибка может возникать в случае окончания лецензии CRM системы или отсутствие прав у бота.'),
    'autopay_2': '🔥 К сожалению, нам не удалось провести платеж по филиалу *%s*!\n\nПожалуйста, обратитесь в поддержку, мы поможем!'
}

system_errors = {
    'system_test': 'Все пошло не по плану!'
}

regular_errors = {
    'reg_tasks3_1': '*Сбой в beauty_bot_regular_tasks3 -> compare_records_from_ycl_with_db!*\n%s',
    'reg_tasks3_2': '*Сбой в beauty_bot_regular_tasks3 -> check_and_warn!*\n%s',
    'reg_tasks_q1': '*Сбой beauty_bot_regular_tasks_q1!*\n %s',
    'reg_tasks_q2': '*Сбой beauty_bot_regular_tasks_q2!*\n %s',
    'reg_tasks3_3': '*Сбой в beauty_bot_regular_tasks3 -> month_stats_sendout_lost!*\n%s',
    'reg_tasks3_4': '*Сбой в beauty_bot_regular_tasks3 -> send_msg_for_tomorrow_autopay!*\n%s',
    'reg_tasks3_5': '*Сбой в beauty_bot_regular_tasks3 -> try_today_autopay!*\n%s',
    'reg_tasks3_6': '*Сбой в beauty_bot_regular_tasks3 -> try_repeat_autopay!*\n%s',
    'short_tasks_1': '*Сбой beauty_bot_short_tasks error -> set_webhook!*\n %s',
    'short_tasks_2': '*Сбой beauty_bot_short_tasks error -> create_cached_bc!*\n %s',
    'short_tasks_3': '*Сбой beauty_bot_short_tasks error -> update_services_categories!*\n %s',
    'short_tasks_4': '*Сбой beauty_bot_short_tasks error -> clearind_DB!*\n %s',
    'short_tasks_5': '*Сбой beauty_bot_short_tasks error -> clear_non_used_instances!*\n %s',
    'short_tasks_6': '*Сбой beauty_bot_short_tasks error -> clear_ins_queues!*\n %s',
    'short_tasks_7': '*Сбой beauty_bot_short_tasks error -> add_charges_sum!*\n %s',
    'short_tasks_8': '*Сбой beauty_bot_short_tasks error -> send_phones_DB!*\n %s',
    'short_tasks_9': '*Сбой beauty_bot_short_tasks error -> Triggers().payment_notification!*\n %s',
    'short_tasks_10': '*Сбой beauty_bot_short_tasks error -> sendouts_24h_stats!*\n %s',
    'short_tasks_11': '*Сбой beauty_bot_short_tasks error -> check_expire_accounts_and_notify_owners!*\n %s',
    'short_tasks_12': '*Сбой beauty_bot_short_tasks error -> backup_all_bot_clients!*\n %s',
    'short_tasks_13': '*Сбой beauty_bot_short_tasks error -> process_birthdays!*\n %s',
    'short_tasks_14': '*Сбой beauty_bot_short_tasks error -> check_and_set_yclients_webhook!*\n %s',
    'short_tasks_15': '*Сбой beauty_bot_short_tasks error -> process_staff_kpi!*\n %s',
    'msgs_runner2_1': '*Сбой messages_runner2 -> async_runner!*\n %s',
    'msgs_runner3_1': '*Сбой messages_runner3 -> async_runner!*\n %s',
    'tlg_msg_runner_1': '*Сбой tlg_msg_runner!*\n %s',
    'tlg_msg_runner_partner_1': '*Сбой tlg_msg_runner_partner!*\n %s',
    'gt_tf_payments_1': '*Сбой в dataLore -> get_tinkoff_payments!*\n%s',
    'amo_1': '*Сбой в amo -> notify_sales_about_first_enable_instance*\n%s',
    'amo_2': 'Не удалось отключить хуки состояния для филиала %s\n\n',
    'payments_4': '*Сбой в handler_beauty -> check_pay -> refund_after_enable_autopay!*\n%s',
    'hb_1': '*Сбой в handler_beauty -> check_time_msg_and_form_req*\nошибка подготовки сообщения v3\n%s',
    'sendout_1': '*Сбой в sendout -> yclients_xlsx*\nsendouts: error: xls read error in sendout.py; message:\n%s',
    'sendout_2': '*Сбой в xls -> get_all_client_names*\nget name error\n%s',
    'autopay_notify': '*Сбой в autopay_notify! Не удалось отправить сообщение для %s*\n%s',
    'autopay_3': '*Сбой в get_autopay! Не удалось провести АП*\n%s',
    'autopay_4': '*Сбой в get_autopay! Не удалось оповестить о неуспешном списании*\n%s',
    'add_bot_client_1': '*Сбой в add_bot_client! Не удалось добавить номер филиала в АМО!*\n%s',
    'create_client_1': '*Сбой активации аккаунта а маркетплейсе*\n%s',
    'th_1': '*Сбой при подсчете статистики за день!*\n%s'
}
