help_msg = '''
👩‍💻 Служба поддержки:

телеграм: @beauty_support_bot

☎️ Позвонить в поддержку: +79581110714

📱 Подписывайтесь на наш канал в ТГ @beauty_bot_rf

Рекомендуйте Бота и получайте по 1 месяцу за каждого кто подключится. Сразу после его оплаты.

Ваша персональная ссылка для приглашений находится в кнопке "Оплата"

Для Вашего удобства у нас появился <a href="https://лк.бьютибот.рф/">💻 Личный кабинет</a>

Ответы на все вопросы по работе с ним Вы можете найти в нашей <a href="http://beautybot.platrum.ru/lk">📖 Базе знаний</a>
'''

start_message = '''
Здравствуйте, я Бьюти Бот. Что я такое?

Я увеличиваю прибыль компаниям, которые используют Yclients для записи клиентов. Каким образом?

👉 Экономлю деньги отправляя не смс, а сообщения в вотсап
👉 Подтверждаю создание записи и напоминаю о ней заранее
👉 Возвращаю клиентов если они не записываются
👉 Пишу постоянным клиентам при открытии записи на следующий месяц
👉 Контролирую администраторов, чтобы они не забывали ответить клиентам
'''

get_forms = 'Чтобы подключиться, напишите в телеграм поддержки: @beauty_support_bot и заполните форму https://forms.yandex.ru/u/61b880fad2e4dc54b1e5d628/'

send_id = 'Ваш ID для подключения бота:\n\n{}'

sendout_warning = '''
*Внимание, очень важно:*
🤔 Любая рассылка несёт в себе риск того, что ваш вотсап заблокируют. Не надо бояться делать рассылки, однако, лучше придерживаться следующих правил:

❗ Не отправляйте сообщения тем, кто вас не знает и не ждёт вашего сообщения. Такие "холодные" клиенты, скорее всего, будут жаловаться на спам и ваш номер может быть заблокирован.
❗ Используйте {name} в тексте сообщения, так вы делаете каждое сообщение уникальным.
❗ Не делайте рассылки с новых номеров вотсапа. Минимальный возраст вотсапа для рассылок - 2 месяца.

Соблюдая эти правила, ваши рассылки всегда будут эффективными.

*Что повышает риск?*
👉 возраст вотсапа: если вотсапу меньше 1.5 месяцев, не рекомендуется делать рассылки вообще
👉 наличие внешней ссылки в тексте

*Мы не несём ответственности в случае блокировки вашего вотсапа*

Видео-инструкция: https://youtu.be/0qoDW13iJJ8
Текстовая инструкция: https://www.notion.so/botsarmy/37ecddbb17584843b4beffd0b2e44821
Примеры текстов рассылок: https://telegra.ph/Primery-tekstov-rassylok-08-09
'''

sendout_get_text = '''
*ШАГ 1 - ЧТО ОТПРАВЛЯТЬ КЛИЕНТАМ?*

Очень рекомендуем использовать в тексте рассылки:
*{name}* - для подстановки имени клиента

Вы можете сделать рассылку в виде:

👉 текста
👉 фото/видео
👉 фото/видео с текстом
❗ Размер файла не может превышать 20 МБ

Отправьте боту текст, фото/видео или фото/видео с подписью которые вы хотите разослать
👇
'''

sendout_get_file = '''
*ШАГ 2 - КОМУ ОТПРАВЛЯТЬ?*

*Скачайте файл с клиентами из Yclients:*

👉 Зайдите в Клиенты - Клиентская база
👉 Задайте филтры чтобы сформировать список нужных клиентов
👉 Справа наверху - скачайте список в Excel


*Если вы сами составляли этот файл а не скачали его из Yclients:*

👉 столбик с именами должен называться "Имя"
👉 столбик с телефонами должен называться "Телефон"


📎 Теперь приложите файл в бота и отправьте 👇
_рассылка не начнётся сразу после загрузки файла, вы сможете ещё раз всё проверить_
'''

sendout_after_test = '''
Тестовое сообщение отправлено на номер {}

Внимание! В тестовом сообщении не подставляется имя, поэтому оно придёт без имени, в рассылке имена подставятся.

Чтобы *начать рассылку* нажмите на кнопку "Начать рассылку" в сообщении выше 👆

Если вы хотите создать рассылку заново, нажмите кнопку "Рассылка" 👇
'''

connect_info1 = '''
*Нажмите кнопку Настройки внизу*
и вы увидите статус вашего подключения


🟢 *Подключён*
Ваш Бот подключён и работает нормально.
'''

connect_info2 = '''
🟡 *Подключается*

Соединение с Ботом потеряно:

- Перезагрузите рабочий телефон с вотсапом
- Нажмите кнопку "Перезагрузить соединение" в Боте

Через 2 минуты Бот подключится.
'''
connect_info3 = '''
🔴 *Отключен*
Бот не подключён к вашему вотсапу.

- В рабочем вотсапе зайдите в Настройки - Связанные устройства - Выйти со всех устройств (если есть) - откроется камера для сканирования
- В телеграме нажмите "Получить QR" и отсканируйте его камерой вотсапа.

Нажмите Настройки чтобы проверить статус подключения
'''

bb_lead_msg1 = '''

🤔 *Что тaкoe Бьюти Бoт и как он пoможет сaлoну?*

Представьте, что вотсап вашего салона возвращает потерявшихся клиентов на автомате, подтверждает клиентов на завтра, а также отправляет все нужные уведомления.

Это и многое другое делает Бьюти Бот.

💳 И это стоит от 1490 руб. в мес без ограничений на количество и длину сообщений.


🤔 *Кто уже работает с Ботом?*

👉 Sahar&Vosk
👉 OldBoy
👉 TOPGUN
👉 Кисточки
👉 Точка Красоты

🤔 *Что именно делает Бот?*

*Во-первых,* Бот сам подтверждает клиентов на завтра, вот такими сообщениями в вотсап 👇
'''

bb_lead_msg2 = '''
Мария, добрый день, это 👸 *Самый Лучший Салон*

Вы записаны к нам на завтра:

👉 на 12-00

к мастеру 👩Елена

На услугу:
▫️ стрижка

Вы подойдёте?
'''

bb_lead_msg3 = '''
Если клиент ответит что подойдёт, то Бот сам изменит статус записи в Yclients на ✔️"клиент подтвердил"

Таким образом, Бот подтверждает всех клиентов на завтра.


*Во-вторых,* Бот возвращает потерявшихся клиентов на автомате. Вот такими сообщениями: 👇
'''

bb_lead_msg4 = '''
Мария, добрый день, это администратор 👸 *Самого Лучшего Салона*

Я посмотрела по программе, Вы так давно не были у нас.

Подобрать вам удобный день и время для записи?
'''

bb_lead_msg5 = '''
Такие сообщения Бот будет отправлять каждый день всем клиентам, кто не был

👉 35, 65 или 95 дней (можно поменять)

и ещё не записан на будущие даты.


Также Бот умеет:
👉 запрашивать отзыв на карты
👉 делать рассылки по вашей базе клиентов
👉 поздравлять с ДР
👉 отправлять сообщения с баллами программы лояльности


Этo и мнoгое другoe Бьюти Бoт делает автоматически.

И этo дeшевлe, чем смc, котoрые никто нe читает.

🤩 *Кaк этo вoзмoжнo?*

Тeпeрь возмoжно! Bы дaёте дoступ Бoтy к вашeму вотcапу и Yclients, далeе бoт всё дeлaeт сам.

В резyльтатe вы пoлучaете прямой достyп к вотcапу клиeнтa и сoздаётe новый кaнaл общeния, котoрый yжe ceйчaс болee эффективный, чeм инcтаграм и yж тем более смс.

💳 *Скoлькo этo cтоит?*

Oт 1490 руб в месяц, количecтво cooбщений не огрaничeно. При этoм, вам нe нужно бoльшe трaтиться нa cмс.

🙋 *Это oкyпитcя?*

Сразу же!

👉 вы начнёте возвращать потерявшихся клиентов на автомате
👉 уменьшите количество ошибок администраторов до 0
👉 снизите расходы на бесполезные смс
👉 повысите рейтинг салона на Яндекс-картах, 2Gis или Google maps
👉 сможете видеть сколько вы заработали с каждой рассылки

🦸‍♂️ *Сложно ли подключить Бoтa?*

Heт, спeциалист пoддержки помoжет вам подключиться зa 10 мин.'''

bb_lead_msg6 = '''
😲 *У нaс ecть индивидyaльное прeдложение для новыx клиeнтoв.*

*Рaсскaзать?*
'''

call_back = '''
🤷️ Извините, мы не принимаем звонки в вотсап

Вы можете позвонить нам прямо сейчас (не через вотсап) по этому номеру:

+79581110714

либо мы сами перезвоним вам чуть позже
'''

msg_not_sent = '''
🆘🆘🆘

Cообщение не отправлено, так как ваш вотсап филиала {} не подключен к интернету.

Что делать?

👉 Отправьте Боту точку .
👉 В самом низу нажмите кнопку Настройки
👉 Следуйте инструкциям
'''

reminder_2nd_day_lead = '''
Добрый день, вы интересовались вотсап-ботом для Yclients

🤔 *Почему он окупится за 3 дня?*

▫️ Он возвращает клиентов на автомате. Видит всех потеряшек за 30, 60 и 90 дней и приглашает их записаться снова.
▫️ Сам подтверждает клиентов на завтра.
▫️ Делает рассылки промо-акций по вашей базе. После рассылки можно посмотреть сколько вы с неё заработали

🤔 *Это всё?*

Нет, ещё он:

▫️ Oтправляет все уведомления (о записи, напоминания, поздравления с ДР)
▫️ Снижает количество ошибок администраторов
▫️ Увеличивает количество хороших отзывов на картах

🤔 *Кто с вами работает и сколько стоит?*

Уже подключили Бота:

🏙️ Sahar&Vosk
🏙️ OldBoy
🏙️ TOPGUN
🏙️ Кисточки
🏙️ Точка Красоты

💳 Стоимость от 1490 руб. в месяц


🎁🎁🎁 _Прямо сейчас мы дарим вам 2 недели использования Бота бесплатно, если вы подключитесь сегодня_

*Интересно было бы попробовать бесплатно и посмотреть сколько Бот заработает для Вас в первые 3 дня?*'''

l1 = 'Добрый день, вчера вы интересовались Бьюти Ботом, который соединяет Yclients и Вотсап.\n\nБот возвращает клиентов на автомате, подтверждает клиентов на завтра а также делает рассылки\n\nТакже он сильно упрощает работу админов\n\nПланируете попробовать Бота бесплатно?'
l3 = 'Добрый день, специально для вас хочу сделать особенное предложение - 14 дней использования Бота бесплатно.\n\nИнтересно было бы попробовать?'
l7 = 'Добрый день, последнее наше предложение - 1 месяц Бьюти Бота бесплатно, если подключаетесь сегодня или завтра.\n\nПлатить ничего не надо, просто первый месяц пользуетесь соверешнно бесплатно.\n\nИнтересно было бы попробовать современные технологии в действии?'
i1 = 'Добрый день, нужна помощь с настройкой Бота по инструкции?\n\nМожем назначить время и дату, когда вы будете у компьютера, созвониться и сделаем всё онлайн.\n\nУдобно было бы так?'
i3 = ''

success_payment_info = '''
💳 Оплата получена за филиал {}, спасибо
*Нравится Бьюти Бот?*
Подарите коллегам 1 месяц бесплатно и получите тоже 1 месяц бесплатно за каждый подключённый салон!
Ваша личная ссылка для рекомендаций:
https://t.me/beauty_support_bot?start=p{}
🎁 Все клиенты, которые подключатся по вашей ссылке, получат 1 месяц бесплатно.
🎁 Вы тоже получите 1 месяц бесплатно за каждый подключенный по вашей ссылке салон
🤓 _Бесплатный месяц будет начислен после первой оплаты салоном их подписки_
Пожалуйста, ответьте на 2 вопроса о Боте
👉 https://clck.ru/gj7iY
'''

offer_autopay = '''
Надоело платить за Бота каждый месяц?
Подключите автоплатёж и мы сами будем списывать оплату. Заранее предупредим что спишем и уведомим что Бот продлён)
подключите прямо сейчас
👇👇👇

'''

success_autopay_info = '''
💳 Ура, автоплатеж за филиал <b>{}</b> успешно подключен!

Оплата за Бьюти Бот будет автоматически списываться каждого {} числа.

Мы будем уведомлять о предстоящем списании заранее, чтобы вы ничего не забыли!
'''

before_autopay_info = '''
Итак, вы собираетесь подключить <b>автоплатеж</b> по филиалу <b>{}({})</b>.
👩 <b>{}</b> сотрудников
💳 <b>{} руб.</b> в месяц

Чтобы подключить автоплатёж, перейдите по ссылке:
👉 <a href="{}">Подключение автоплатежа</a>

Мы спишем и вернём 2 руб., а далее будем списывать оплату за Бота с этой карты ежемесячно.

🔥 открывайте ссылку с того устройства, с которого будете оплачивать
🔥 ссылка живёт всего 1 час, если прошло больше времени — просто сформируйте новую
'''

disable_autopay_info = '''
Автоплатёж по филиалу <b>{}</b> на сумму {}р. отключен

Вы можете легко подключить его снова, нажав соответствующую кнопку в меню «Оплата».
'''

success_refund_info = '''
Возврат тестового платежа прошёл успешно!
<i>Средства могут поступить на ваш счёт не сразу. Точные сроки возврата зависят от вашего банка.</i>
'''

failed_refund_info = '''
Ошибка при проведении возврата по филиалу {}({}, {})</b>!
Пожалуйста, попробуйте снова или обратитесь в Службу поддержки, мы поможем!
'''

failed_autopay_info_dev = '''
<b>Не прошел автоплатеж по филиалу {}({}, {})</b>
Статус: {}
Причина: {}
'''

failed_autopay_info_user = '''
🔥 <b>К сожалению, нам не удалось произвести автоплатёж по филиалу {}({}, {})</b>

Пожалуйста, проверьте банковскую карту, которую вы указали для автосписаний!
Изменить карту для автосписаний можно в меню «Оплата».

Завтра мы снова попробуем списать оплату за Бьюти Бота и уведомим вас о статусе платежа.
'''

failed_autopay_info_user_WA = '''
🔥 К сожалению, нам не удалось произвести автоплатёж по филиалу {}({}, {})

Пожалуйста, проверьте банковскую карту, которую вы указали для автосписаний!
Изменить карту для автосписаний можно в меню «Оплата».

Завтра мы снова попробуем списать оплату за Бьюти Бота и уведомим вас о статусе платежа.
'''

not_enough_money_for_autopay = '''
🔥 <b>К сожалению, нам не удалось произвести автоплатёж по филиалу {}({}, {})</b>

Недостаточно средств на карте, которую вы указали для автосписаний.

Пожалуйста, проверьте баланс карты и нажмите на кнопку под этим сообщением, чтобы снова попробовать произвести оплату..
'''

not_enough_money_for_autopay_WA = '''
🔥 К сожалению, нам не удалось произвести автоплатёж по филиалу {}({}, {})

Недостаточно средств на карте, которую вы указали для автосписаний.
'''

again_failed_autopay = '''
🔥 <b>К сожалению, нам не удалось произвести автоплатёж по филиалу {}({}, {})</b>

Пожалуйста, проверьте банковскую карту, которую вы указали для автосписаний!

Мы больше не будем пытаться списать средства автоматически. Чтобы оплатить Бьюти Бота — попробуйте произвести оплату другим способом.
Если возникнут проблемы — обращайтесь в поддержку, мы поможем!
'''

warning_at_one_day_before = '''
Добрый день!

Напоминаем, что завтра будет произведено автоматическое списание за Бьюти Бот на филиале <b>{}({})</b>
💳 <b>{} руб.</b>

🔥 Пожалуйста, убедитесь, что необходимая сумма есть на карте, которую вы привязали для автосписаний.
'''

warning_at_one_day_before_WA = '''
Добрый день!

Завтра будет произведено автоматическое списание за Бьюти Бот на филиале {}({})
💳 {} руб.

🔥 Пожалуйста, убедитесь, что необходимая сумма есть на карте, которую вы привязали для автосписаний.
'''

autopay_description = '''Автооплата за Бьюти Бота на 1 мес для филиала {} {}'''

autopay_item_description = '''Бьюти Бот на 1 мес для филиала {}'''

info_if_enable_autopay = '''
<b>{}</b>, филиал № {}

👩 {} сотрудников

Подключен автоплатеж:
💳 <b>{} руб.</b>

💳 Последние 4 цифры карты: {}
Списание: каждое {} число месяца
'''

change_card = '''
Вы собираетесь <b>изменить карту</b> для автоплатежа по филиалу <b>{}({})</b>.
👩 <b>{}</b> сотрудников
💳 <b>{} руб.</b> в месяц

Чтобы изменить карту, перейдите по ссылке:
👉 <a href="{}">Смена карты</a>

Мы спишем и вернём 2 руб., а далее будем списывать оплату за Бота с этой карты ежемесячно.

🔥 открывайте ссылку с того устройства, с которого будете оплачивать
🔥 ссылка живёт всего 1 час, если прошло больше времени — просто сформируйте новую
'''

multi_pay_msg = '''
Вы можете внести оплату сразу по всем филиалам по ссылкам ниже!
🔥 открывайте ссылку с того устройства, с которого будете оплачивать
🔥 срок жизни ссылок 1 час

🔥 обратите внимание, данный способ оплаты учитывает только филиалы без подключенного автоплатежа

<b>Выберите период оплаты:</b>

👉 <a href="{}">1 месяц</a>

👉 <a href="{}">3 месяца</a>
<i>с бонусным периодом {} недели</i>

👉 <a href="{}">6 месяцев</a>
<i>с бонусным периодом {} недель</i>

👉 <a href="{}">12 месяцев</a>
<i>с бонусным периодом {} недели</i>
'''

BF_autopay = """Ура!

Вы подключили автоплатеж и мы начислили вам 1 неделю!

Желаем полной записи!"""

pay_msg = """🔥 открывайте ссылку с того устройства, с которого будете оплачивать
🔥 срок жизни ссылок 1 час

<b>Выберите период оплаты:</b>

👉 <a href="{}">1 месяц</a>

👉 <a href="{}">3 месяца</a>
<i>с бонусным периодом {} недели</i>

👉 <a href="{}">6 месяцев</a>
<i>с бонусным периодом {} недель</i>

👉 <a href="{}">12 месяцев</a>
<i>с бонусным периодом {} недели</i>

Ссылка для приглашения:
{}"""

pay_msg_header = '''<b>{}</b>, филиал № {}

👩 <b>{}</b> сотрудников
💳 <b>{} руб.</b> в месяц
оплачен до: {}

'''

pay_msg_header_s_a = '''<b>{}</b>

💳 тариф <b>{} руб.</b> в месяц
оплачен до: {}

'''

instance_fail = '''
Внимание! Так как ваш Бот отключался за неоплату, вам нужно заново отсканировать QR код.

👉 зайдите в вотсап на телефоне
👉 откройте меню вотсапа, далее - Связанные (привязанные) устройства
👉 нажмите "привязка устройства", откроется камера для сканирования QR кода
👉 запросите QR, нажмите кнопку "Получить QR" в настройках
👉 отсканируйте полученный QR код камерой вотсапа
'''

create_review_group = '''👋 Добрый день, эта группа создана автоматически 🤖Бьюти Ботом.

Сюда Бот будет скидывать все негативные отзывы и оценки, которые поставят ваши клиенты.

Вы также можете добавить сюда ваших сотрудников.

Если вы хотите, чтобы Бот присылал эту информацию в другую группу вотсапа, просто отправьте в ту группу сообщение с текстом:

#otziv%s'''

get_qr_message = '''⏳ QR код действителен в течении 20 сек

🔥 Если после сканирования вы видите ошибку, скорее всего, QR код протух. Просто получите новый.

🧾 Отсканировав QR, вы даёте согласие на полный доступ Бьюти Бота к вотсапу'''

messages = {
    'select_setup': 'Выберите настройку:',
    'pay_message': 'Аккаунт %s оплачен до %s по тарифу %s',
    'choose_lenght': 'На аккаунте %s %i сотрудников. Ваш тариф %s.\nПродлить на:',
    'run_out': 'Срок действия аккаунта %s истек %s',
    'check_pay': 'Тариф %s успешно оплачен до %s',
    'first_pay': 'Аккаунт %s не оплачен.\nСтоимость зависит от количества сотрудников:\nДо 10 сотрудников 1690 р/мес\nДо 30 сотрудников 2190 р/мес\nСвыше 30 сотрудников 2690 р/мес\nПеред оплатой проверьте свои данные Yclients',
    'module_selection': 'Выберите услугу, которую хотите изменить на аккаунте %s',
    'switch_acc': 'Текущий аккаунт: %s\nВыберите аккаунт, который хотите сделать текущим:',
    'one_acc': 'У вас имеется только один аккаунт: %s',
    'ignor_list': 'Номер #t%s более не отслеживается\nВы можете его вернуть в настройках',
    'not_pay': 'Аккаунт не оплачен',
    'black_list': 'Номер #t%s более не участвует в рассылке акаунта %s\nВы можете его вернуть в настройках',
    'fail_phone': 'Номер указан неверно. Попробуйте еще раз',
    'no_user_rights': 'У вас нет прав, обратитесь к руководству',
}

tmp_messages = {
    'stats_buttons_template': 'Статистика шаблона',
    'on_template': 'Шаблон %s включён и теперь будет отправляться клиентам',
    'off_template': 'Шаблон %s выключен и теперь не будет отправляться клиентам',
    'accept_changes_template': 'Шаблон отредактирован',
    'decline_changes_template': 'Изменения отклонены',
    'no_params_template': 'Нет таких параметров',
    'change_param_template': 'Параметр изменен',
    'no_stats_data_template': 'Нет данных статистики шаблона',
    'no_last_version_stats_template': '🤷‍♀️ Статистика последней версии шаблона пока недоступна',
    'no_phone_blacklist_template': 'Вы не ввели номера. Повторите ввод списка номеров для добавления в ЧС шаблона %s',
    'add_phone_numbers_blacklist_template': 'Номера добавлены',
    'empty_time_template': 'Вы не ввели параметр. Он должен быть числом. Поворите ввод нового времени шаблона',
    'error_time_template': 'Вы ошиблись в вводе пераметра. Он должен быть введен в формате часы, минуты (20.00 или 9 00 или 15:00)',
    'edit_template': '❗<b>Отправьте Боту новый текст шаблона</b>\n\nВы можете подставить в сообщение любую информацию, для этого вставьте в текст любой из ключей:\n\
        {name} - Для подстановки имени клиента\n\
        {day_month} - Для подстановки даты и месяца (12 декабря)\n\
        {day_of_week} - Для подстановки дня недели\n\
        {start_time} - Время начала услуги\n\
        {end_time} - Время окончания услуги\n\
        {master} - Имя мастера\n\
        {price} - Цена\n\
        {services} - Услуга или список услуг\n\
        {review_link} - Ссылка на Yclients для отзыва\n\n\
        {record_link} - Ссылка на Yclients на удаление записи клиентом\n\n\
        Внимание! Отправьте только текст сообщения без номера шаблона, параметров... Только тот текст, который хотите заменить.❗',
    'edit_confirm_record_text': "❗Введите тест сообщения подтверждения записи.\n Тескт не должен содержать ключей.❗",
    'confirm_tmp_msg': 'Вы точно хотите заменить текст шаблона %s на?\n\n<b>%s</b>',
    'edit_template_media': '❗Отправьте медиафайл\nРазмер медиафайла не должен превышать 20 Мб❗',
    'confirm_tmp_media': 'Вы точно хотите добавить медиафайл к шаблону %s?',
    'delete_template_media': 'Вы точно хотите удалить медиафайл из шаблона %s?',
    'delete_tmp_msg': 'Вы точно хотите удалить сообщение из шаблона %s%s?',
    'template_stats_message': '📊 <b>Статистика последней версии шаблона %s:</b>\n\n\
<b>Дата изменения</b>\n%s\n\n\
<b>Отправлено</b>\n%i сообщений\n\n\
<b>Ответили</b>\n%i кл. (%i %% )\n\n\
<b>Записалось</b>\n%i кл. (%i %% )\n\n\
<b>Заработано после отправки шаблона</b>\n%i руб.\n\n\
<b>Заработано с одного сообщения</b>\n\n%i руб.',
    'full_stats_template': 'Ваша статистика рассылок',
    'template_blacklist_with_phone': 'В вашем ЧС для шаблона %s: %s\n\n\
Введите номера, которые хотите добавить в Чёрный список через ,',
    'template_blacklist': 'В ваш ЧС для шаблона %s не добавлено номеров\n\n\
Введите номера, которые хотите добавить в Чёрный список через ,',
    'template_blacklist_phone_mistake': 'У вас ошибка в номере %s проверьте, что все номера записаны через запятую и содержат правильное количество цифр (11 для номеров с 8ки и 12 для номеров с +7)',
    'media_link_template': '    - Ссылка на медиафайл: %s\n',
    'start_message_sms_text': '\n\n💬 <b>Смс-текст:</b>\n%s',
    'start_message_confirm_text': '\n\n<b>✅Текст при подтверждении</b>\n%s',
    'start_message_declined_text': '\n\n<b>❌Текст при отмене</b>\n%s',
    'start_message_template': '<b>Шаблон № %s</b>\n\n⚙️ <b>Параметры шаблона:</b>\n%s\n⌨️ <b>Вотсап-текст шаблона:</b>\n%s',
    'check_msg_keys_template': 'Проверьте ключи и введите текст шаблона ещё раз',
    'check_msg_brace_template': 'Проверьте скобки {}',
    'dumb_message_template': 'Похоже, вы ввели не сам текст шаблона, а также служебную информацию.\n\nЧтобы изменить текст шаблона, отправьте боту только вотсап-текст 👇',
    'error_after_template': 'Вы ошиблись в вводе пераметра. Он должен быть введен в формате одного числа (Пример: 1 или 32 или 64, параметр может быть любым числом)',
    'review_messages': '<b>Шаг №%i</b>\n\n<b>Параметры:</b>\n%s\n<b>Текст</b>\n%s',
    'review_messages_text': '<b>Шаг №%i</b>\n\n<b>Параметры:</b>\n%s\n<b>Текст при хороших оценках</b>\n%s\n\n<b>👎 Текст при плохих оценках</b>\n%s',
    'review_messages_info': 'Минимальное количество шагов: 2\nПроверьте наличие ссылок в последнем сообщении!\nДля того чтобы добавить/удалить шаг или изменить минимальную оценку обратитесь в поддержку',
    'edit_review_template': 'Введите текст',
    'edit_review_link': 'Вставьте ссылку на отзыв',
    'no_param': 'Не найден параметр. Обратитесь в поддержку',
    'no_review_templates': 'Нет шаблонов данного типа.\n\nЕсли хотите создать, нажмите кнопку 👇',
    'lk_tmp_link': '\n\nВы знали, что можете отредактировать шаблон в личном кабинете?\n👉 <a href="{}">Редактировать в личном кабинете</a>'
}

BF_sendout_promo = """Ура!

Вы сделали первую рассылку и мы начислили вам 1 неделю!

Желаем полной записи!"""

review_messages = {
    'admin_warn': 'У клиента wa.me/%s есть вопросы',
    # 'bad_est': 'Клиент %s поставил оценку %s и написал комментарий:\n\n%s',
    'bad_est': '🔥 *НОВЫЙ ОТЗЫВ*\n\n*%s* wa.me/%s \n*%s* визитов\n\n*На вопрос:*\n%s\n\n*Ответила:*\n%s',
    'fail_rev': '🔥 *НОВЫЙ ОТЗЫВ*\n\n*%s* wa.me/%s\n*%s* визитов\n\n*Написала:*\n\n%s',
    'rev_create': 'Шаблоны добавлены\n\nПожалуйста, проверьте текст созданных шаблонов',
    'no_tmp': 'Мы не нашли у вас ссылок на отзывы, подставьте их в текст(Настройки -> Цепочка отзывов -> Шаг 3 -> Изменить текст)',
    'none_record': '❌Cообщение отзыва не отправлено на номер %s\nНе найдена запись в Yclients'
}

sendout_messages = {
    'no_last_version_stats_sendouts': '🤷‍♀️ Статистика рассылок пока недоступна',
    'no_data_sendouts': 'Нет данных статистики рассылок',
    'full_stats_sendouts': 'Ваша статистика рассылок',
    'choose_sendout_action': 'Выберите действие: ',

    'sendout_stats_message': '📊 <b>Статистика последней рассылки:</b>\n\n\
<b>Текст</b>\n{}\n\n\
<b>Дата отправки</b>\n{}\n\n\
<b>Всего</b>\n{} сообщений\n\n\
<b>Ответили</b>\n{} чел. ({} % )\n\n\
<b>Записалось</b>\n{} ({} % )\n\n\
<b>Заработано:</b>\n{} руб.\n\n\
<b>Заработано с одного сообщения</b>\n{} руб.',

    'no_pay_sendouts': 'На аккаунте {} закончился оплаченный период.\n\nЧтобы оплатить, нажмите "Оплата"',
    'off_sendouts': 'На аккаунте {} отключены рассылки.',

    'choose_filial_sendouts': 'Выберите филиал, для которого хотите сделать рассылку:',
    'no_access_sendouts': 'Рассылки доступны только на платном тарифе Бота',
    'no_text_sendouts': 'Текст сообщения не обнаружен, пришлите текст сообщения для рассылки',
    'long_text_sendouts': 'Длина текста рассылки больше 2000 знаков. Пожалуйста, сократите текст и отправьте ещё раз.',
    'file_message_sendouts': 'Либо вы можете вставить свои данные в этот шаблон, а затем загрузить файл шаблона в бота.',
    'number_recipients_sendouts': 'Вы собираетесь отправить рассылку для {} получателей',
    'number_message_in_day_sendouts': '\n\n🔥 Внимание, вы можете отправить в рассылке {} сообщений в день, остальные {} сообщений будут отправлены в это же время в следующие {} дня',
    'cancel_sendouts': 'Рассылка отменена',
    'start_sendouts': 'Рассылка начата\n\nКак остановить рассылку?\n\nНажмите кнопку 👇',
    'stop_sendouts': 'Рассылка остановлена',
    'send_yourself_sendouts': 'Отправить тест себе',
    'decline_sendouts': 'Отменить рассылку',
    'run_sendouts': 'Начать рассылку',
    'file_too_large': 'Ваш файл более 20 МБ, используйте сжатие или выберите другой файл'
}

edit_parametr = {
    'before_start': 'Отправьте Боту одну цифру, за сколько часов до записи будет отправляться данный шаблон. Например, если вы отправите 2, то данный шаблон будет отправляться за 2 часа до записи',
    'after_end': 'Отправьте Боту одну цифру, через сколько часов после записи будет отправляться данный шаблон. Например, если вы отправите 2, то данный шаблон будет отправляться через 2 часа после записи',
    'all_day_recs_notifications': 'Отправьте Боту время, в которое будет отправляться данный шаблон. Например, если вы отправите 20.00, то данный шаблон будет отправляться в 20.00'}

template_keys = {'before_start': 'за %i ч. до услуги',
                 'after_end': '%i ч. после услуги',
                 'categories': 'Для категорий услуг: %s',
                 'services': 'Услуги: %s',
                 # 'online': 'Онлайн запись: %b',
                 'visits': 'Количество визитов: %s',
                 'visits_frequency': 'Отправлять через каждые %i визитов',
                 'all_day_recs_notifications': 'Всем клиентам за дату %s день от сегодня, отправка в %s',
                 'event': '',
                 'record_create': 'При создании записи %s',
                 'record_delete': 'При удалении записи %s',
                 'record_paid': 'При оплате записи %s',
                 'record_update': 'При изменении записи %s',
                 'record_canceled': 'При отмене записи %s',
                 'integration': 'При интеграции %s',
                 'attendance': 'Если статус записи: %s',
                 'got_records_after': '%s',
                 'got_records_before': '%s',
                 'online': '%s',
                 'client_category': 'Для категорий клиентов: %s',
                 'client_have_abonement': '%s'}

reverse_template_keys = {'categories': 'Для категорий услуг кроме: %s',
                         'services': 'Услуги кроме: %s',
                         'attendance': 'Если статус записи кроме: %s',
                         'client_category': 'Для категорий клиентов кроме: %s'}

type_msg = {'est': 'Ожидает оценку', 'text': 'Отправляем ссылку на отзыв'}

review_template_keys = {
    'format': 'Тип ответа: %s',
    # 'valid':'Минимально допустимое значение: %s',
    'link': 'Ссылка на отзыв: %s',
    'after_end': 'Отправляется через %i ч. после окончания'
}

attendance = {-1: 'клиент не пришёл',
              0: 'ожидание клиента',
              1: 'клиент пришёл',
              2: 'клиент подтвердил'}

true_keys = {'got_records_after': 'Если записан в будущем',
             'got_records_before': 'Если записан в прошлом',
             'online': 'Если онлайн-запись',
             'client_have_abonement': 'Если есть абонемент у клиента'
             }

false_keys = {'got_records_after': 'Если еще не записан в будущем',
              'got_records_before': 'Если не записан в прошлом',
              'online': 'Если не онлайн-запись',
              'client_have_abonement': 'Если нет абонемента у клиента'
              }

default_review_messages = {
    'step1': '{name}, спасибо, что доверяете нам!\n\n\
Пожалуйста, подскажите, вам понравилась работа мастера 👩{master}?',
    'step2': 'Спасибо, теперь оцените, пожалуйста, сервис салона (работа администратора, атмосфера)',
    'step3': 'Спасибо за высокие оценки, мы стараемся ради таких приятных моментов 😍\n\n\
Будем благодарны если также оставите небольшой отзыв по одной из следующих ссылок:\n\n',
    'fail_text': 'Жаль, что вам не все понравилось, напишите, что мы могли бы исправить',
    'master_review': 'отзыв мастеру 👩{master} {review_link}',
    'add_WA_group': 'Группа успешно добавлена!\n\nНовые отзывы для {} теперь будут приходить в эту группу',
    'no_branch_group': 'Не найден филиал {}, проверьте введеные данные! Необходимо отправить сообщение в формате: \n\n##otziv123456\n\nгде 123456 - номер вашего филиала'
}

pay_messages = {
    'pay_message_1': 'Вы можете сформировать общий счет по всем филиалам с ИНН %s:\n%s',
    'pay_message_2': ('*Будет сформирован общий счет*\n\n *%s* филиалов\n'
                      '💳 *%s руб.* в месяц\n\nФилиалы в счете:\n %s\n\nВыберите период оплаты'),
    'link_msg': 'Оплата Бьюти Бота на {} мес для филиала {} {}',
    'link_msg_bonus': 'Оплата Бьюти Бота на {} мес. с бонусным периодом {} нед. для филиала {} {}'
}

bill_text = {
    'no_bill_data': 'Нет данных для генерации счета. Обратитесь в поддержку',
    'service_name_1': 'Оплата Бьюти Бота на %s месяцев, ',
    'service_name_2': 'со скидкой %s%% ',
    'service_name_3': 'для филиала %s',
    'service_name_4': 'с бонусным периодом %s недель ',
    'service_name_5': 'для филиалов %s',
    'cost_error': 'Проблема с оплатой %s',
    'pay_error': 'Что-то пошло не так, попробуйте позже',
    'send_bill': 'Счет на оплату аккаунта %s\n\nПосле оплаты счёта, пожалуйста, скиньте платёжку в телеграм поддержки @beauty_support_bot и мы сразу продлим вам Бота'
}

text_est = {'Не понравилось': 1, 'Сложно сказать': 3, 'Понравилось': 5}

rev_extra_text = '\n\nОтправьте свою оценку:\n1 - 😍 Понравилось\n2 - 😐 Сложно сказать\n3 - 🤬 Не понравилось'

text_est_2 = {'1 - 😍 Понравилось': 5, '2 - 😐 Сложно сказать': 3, '3 - 🤬 Не понравилось': 1}

go_to_tg = 'Извините, поддержка в вотсап больше не осуществляется.\n\nПожалуйста, напишите в бота поддержки в телеграм, спасибо\n\n👉 https://t.me/beauty_support_bot'

support_review = '''Добрый день, вчера вы обращались в поддержку Бьюти Бота

Помогите, пожалуйста, понять как справился оператор поддержки, поставьте вашу оценку 👇
'''

ycl_recs = '''Номер филиала: %i
Номер записи: %i
Услуги: %s
Сотрудник:
    ID %i
    Имя %s
Клиент:
    ID %i
    Имя %s
    Номер %s
    Визитов %i
Время визита: %s
Время создания: %s
Подтверждение: %i
Последнее изменение: %s
Время окончания: %s'''

add_to_group = '''Чтобы мы могли общаться, пожалуйста, дайте Боту доступ к сообщениям в группе:

1. нажмите на название группы наверху
2. в открывшемся окне справа наверху нажмите 3 точки
3. нажмите управление группой
4. нажмите администраторы
5. внизу - добавить администратора
6. выберите Бьюти Бот Поддержка
7. внизу - закрыить, далее - сохранить
'''

group_rights = '🥳 Всё получилось, пожалуйста, напишите ваш вопрос'

partner_welcome = '🥳 Здравствуйте, вы пришли по рекомендации, и мы рады подарить вам 1 месяц бесплатно!\n\nУ вас есть вопросы или вы готовы подключиться сейчас?\n\nЭто займёт 15 мин.'

settings_text = {
    'auth_WA': '\n🟢 Подключён\n\nинфо: /connect_help',
    'loading_WA': '\n🟡 Подключается\n\nЧто делать?\n\n- перезагрузите рабочий телефон\n- одновременно нажмите кнопку ниже "Перезагрузить соединение"\n\nЧерез 2 минуты Бот подключится\n\nинфо: /connect_help',
    'conflict_WA': '\n🖥️ Открыт на компьютере или другом устройстве\n\nЧто делать?\n\n- нажмите внизу кнопку "Использовать здесь"\n\nЧерез 2 минуты Бот подключится\n\nинфо: /connect_help',
    'no_pay': '\n💳 не оплачен',
    'got_QR_WA': '\n🔴 Отключен\n\n👉 зайдите в вотсап на телефоне\n👉 откройте меню вотсапа, далее - Связанные (привязанные) устройства\n👉 нажмите "привязка устройства", откроется камера для сканирования QR кода\n👉 запросите QR, нажмите кнопку "Получить QR" под этим сообщением\n👉 отсканируйте полученный QR код камерой вотсапа\n',
    'error_WA': 'Ошибка проверки статуса подключения, обратитесь в поддержку'
}

partner_enter = '''
🥳 Здравствуйте, вы пришли по рекомендации, и мы рады подарить вам 🎁 *1 месяц бесплатно!*

У вас есть вопросы или вы готовы подключиться сейчас?

Это займёт 15 мин.
'''

get_promo = '''
Чтобы *получить бонус*, при подключении укажите:

👉 ваш телеграм айди *{}*
👉 ваш промокод *{}*
'''

paid_notification = {
    'days_2': '🔥 Добрый день,{}\nПришло время продлить Бота, потому что послезавтра заканчивается оплата для филиала *{}*\n\nСсылки на оплату можно получить в боте, *кнопка Оплата*\n\nПерейти в бота\n👉 https://clck.ru/Xmcpu',
    # 'days_2': '🔥 Добрый день, послезавтра заканчивается оплата Бьюти Бота для филиала *{}*\n\nСсылки на оплату можно получить в боте, *кнопка Оплата*\n\nПерейти в бота\n👉 https://clck.ru/Xmcpu',
    'days_0': '🔥 Добрый день, сегодня заканчивается оплата и Бьюти Бот перестанет работать для филиала *{}*\n\nСсылки на оплату можно получить в боте, *кнопка Оплата*\n\nПерейти в бота\n👉 https://clck.ru/Xmcpu',
    'days_0_test': '🔥 Добрый день,{}\nCегодня заканчивается оплата и Бьюти Бот перестанет работать для филиала *{}*\n\nСсылки на оплату можно получить в боте, *кнопка Оплата*\n\nПерейти в бота\n👉 https://clck.ru/Xmcpu',
    'test_0_sales': 'Сегодня последний день после теста: {}, телефон {}',
    'bot_review': 'Добрый день, подскажите, как ведёт себя Бот?\n\nЕсть ли какие-то вопросы или сложности?\n\n🤗 Будем рады помочь',
    'acc_stop': '🔥🔥🔥 Бьюти Бот не работает для филиала {}',
    'no_pay_3_days': 'Не оплатили после 3 дней: {}, телефон {}',
    'sendout_stats': '\n👉 запустил {} массовых рассылок, после которых вы получили записей на {} руб.',
    'template_stats': '\n👉 вернул вам {} клиентов, которые принесли вам {} руб.'
    }

after_auth = '''
У вас вопрос?
👉 напишите его сюда

Хотите подключить Бьюти Бота?
👉 ознакомьтесь с инструкцией https://бьютибот.рф/instruct
'''

market_review = '''
💳 Оплата получена, спасибо, что выбрали Бьюти Бот

Будем очень благодарны, если вы оставите отзыв о нас в маркетплейсе Yclients:
👉 https://yclients.com/e/beauty_bot (вкладка Отзывы)

🙏 Это очень важно для нас, заранее спасибо!
'''

instruct_msg = '''
🙏 Спасибо что выбрали Бьюти Бот!

Для продолжения подключения:

1. Активируйте Бота в Yclients:
👉 https://yclients.com/e/beauty_bot

2. Заполните анкету:
👉 https://forms.yandex.ru/u/61b880fad2e4dc54b1e5d628/

При заполнении анкеты укажите ваш telegram_id:
👉 {}

Если у вас есть вопросы, пишите прямо сюда, будем рады помочь.
'''

marketplace_msg = '''
Для продолжения подключения:

Заполните анкету:
👉 https://forms.yandex.ru/u/61b880fad2e4dc54b1e5d628/

При заполнении анкеты укажите ваш telegram_id:
👉 {}

Напишите прямо сюда в чат, что отправили анкету, мы подключим вас максимально быстро.
'''

Partner_messages = {
    'child': '🙏 Спасибо что выбрали Бьюти Бот!\n\n\
Вы пришли по рекомендации, поэтому у нас подарок, Вы получаете:\n\n\
🎁 {}\n\nЧтобы получить подарок, \
при подключении укажите промокод <b>{}</b>\n\nГотовы подключиться? Это займёт 15 мин.\n\n\
👉 Инструкция по подключению: https://бьютибот.рф/instruct\n\n\
Если будут вопросы, пишите их сюда, будем рады помочь 🤗',

    'start': '🟢 #салон_{} обратился по вашей рекомендации.\n\nМы оповестим вас если он подключится',
    'add': '⭐ Новое подключение #салон_{}\n\nФилиал: {}',
    'pay': '💳 Новая оплата #салон_{}\n\nФилиал: {}\n\nСумма: {} руб.'
}
