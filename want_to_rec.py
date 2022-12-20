want_words = [
    'запись',
    "запис",
    'записаться',
    'записать',
    'запиши',
    "запишусь",
    'есть',
    'на какое время',
    'хотел бы',
    'хотела бы',
    'когда',
    "можно",
    "хочу",
    "свободн",
    "окно",
    "окошк",
    "уточн",
    "расскаж",
    "интерес",
    "услуг",
    "хоч"
]

neutral_words = [
    'отмен',
    ' не ',
    'не ',
    'перенес',
    'перенос',
    'перенес',
    'пока',
    'подвину',
    'измен',
    'проще',
    'перезап',
    'запишу',
    'извини',
    'вынужд',
    'через',
    'спишемся',
    'удали',
    'напиш',
    'сообщу',
    'скажу',
    'рано',
    'поменя',
    'перепишите',
]


def find_rec_desire_in_text(text):
    want = [True if want_word in text.lower() else False for want_word in want_words]
    want = True if True in want else False
    neutral = [True if neutral_word in text.lower() else False for neutral_word in neutral_words]
    neutral = True if True in neutral else False

    if not want and not neutral:
        return {'result': 'neutral'}

    if want and not neutral:
        return {'result': 'yes'}

    return {'result': 'neutral'}
