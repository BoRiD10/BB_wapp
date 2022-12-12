confirm_words = [
    'да',
    'подтверждаю',
    'в силе',
    'буду',
    'будем',
    'обязательно',
    'прид',
    'прийд',
    'подойд',
    'конеч',
    'хорошо',
    'я у вас',
    'ок',
    '+',
    'приед',
    'подъед',
    '👍',
    '👌',
    'da',
    'yes',
    'пойд',
    'несомнен',
    '➕',
    'разумеется',
    'угу',
    'ага',
    'плюс',
    'אגיע',
    'מגיעה',
    'אני באה',
    'אני בא',
    'באה',
    'בא',
    'מאשרת הגעה',
    'מאשרת',
    'זוכרת',
    'ברור',
    'כן',
    'בטח',
    'верно',
    '✔️',
    '☑️'
]

neutral_words = [
    'отмен',
    ' не ',
    'не ',
    'перенес',
    'перенос',
    'перенес',
    'пока',
    'болею',
    'заболе',
    'подвину',
    'измен',
    'задерж',
    'проще',
    'перезап',
    'запишу',
    'отказ',
    'извини',
    'вынужд',
    '?',
    'занят',
    'через',
    'спишемся',
    'отъезд',
    'удали',
    'напиш',
    'течен',
    'сообщу',
    'скажу',
    'простыл',
    'простуд',
    'рано',
    'поменя',
    'перепишите',
]

decline_words = [
    '➖',
    '❌',
    'нет',
    '-'
]


def find_agree_in_text(text):
    """Ищет согласие или подтверждение записи в тексте, не учитывает регистр"""
    # ищем слова согласия
    yes = [True if yes_word in text.lower() else False for yes_word in confirm_words]
    yes = True if True in yes else False
    # ищем слова отрицания
    neutral = [True if neutral_word in text.lower() else False for neutral_word in neutral_words]
    neutral = True if True in neutral else False
    # ищем символ отмены записи
    decline = [True if d_word == text.lower() else False for d_word in decline_words]
    decline = True if True in decline else False

    if decline:
        return {'result': 'declined'}

    if yes == False and neutral == False:
        return {'result': 'neutral'}

    if yes == True and neutral == False:
        return {'result': 'yes'}

    if yes == True and neutral == True:
        return {'result': 'neutral'}

    if yes == False and neutral == True:
        return {'result': 'neutral'}

    return {'result': 'neutral'}

# print(find_agree_in_text('Здравствуйте, а я стояла я листке ожидания и я уже сходила к вам в июне)'))
