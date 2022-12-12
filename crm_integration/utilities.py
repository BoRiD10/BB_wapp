from datetime import datetime, timedelta


def fix_data_phone_in_loop(data, crm_name):
    """
    Returns a list of corrected dictionaries data and phone
    :param data:
    :param crm_name:
    :return:
    """
    check_client = [rec_data for rec_data in data['data'] if rec_data.get('client', None) is not None and rec_data['client'].get('id', None) is not None and rec_data['client']['phone'] != '']
    for fix_data in check_client:
        fix_data['datetime'] = fix_data['datetime'][:-6]
        fix_data['create_date'] = fix_data['create_date'][:-6]
        fix_data['last_change_date'] = fix_data['last_change_date'][:-6]
        date_time_str = fix_data['datetime']
        dt_date = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        length = fix_data['length']
        end_time = (dt_date + timedelta(seconds=length)).isoformat()
        fix_data['end_time'] = end_time
        fix_data['name'] = crm_name
        if fix_data['client']['phone'].isdigit() and not fix_data['client']['phone'].startswith('8'):
            continue
        elif fix_data['client']['phone'].startswith('+'):
            fix_data['client']['phone'] = fix_data['client']['phone'].replace('+', '')
            continue
        elif fix_data['client']['phone'].startswith('8'):
            fix_data['client']['phone'] = fix_data['client']['phone'].replace('8', '7')
            continue
    return check_client

def fix_utc_date(data):
    if data.get('data'):
        data['data']['datetime'] = data['data']['datetime'][:-6]
        data['data']['create_date'] = data['data']['create_date'][:-6]
        data['data']['last_change_date'] = data['data']['last_change_date'][:-6]
        return data
    else:
        data['datetime'] = data['datetime'][:-6]
        data['create_date'] = data['create_date'][:-6]
        data['last_change_date'] = data['last_change_date'][:-6]
        return data


def end_time_delta(data):
    """
    Accepts Json adds end_time
    :param data: json
    :return: obj json
    """
    if data.get('data'):
        date_time_str = data['data']['datetime']
        dt_date = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        length = data['data']['length']
        end_time = (dt_date + timedelta(seconds=length)).isoformat()
        data['end_time'] = end_time
        return data
    else:
        date_time_str = data['datetime']
        dt_date = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        length = data['length']
        end_time = (dt_date + timedelta(seconds=length)).isoformat()
        data['end_time'] = end_time
        return data


def fix_number(data):
    """
    Accepts a string with a phone number.
    :param data:
    :return: str phone 7xxxxxxxxx
    """
    if data.get('data'):
        if data['data']['client']['phone'].isdigit() and not data['data']['client']['phone'].startswith('8'):
            return data
        elif data['data']['client']['phone'].startswith('+'):

            data['data']['client']['phone'] = data['data']['client']['phone'].replace('+', '')
            return data

        elif data['data']['client']['phone'].startswith('8'):
            data['data']['client']['phone'] = data['data']['client']['phone'].replace('8', '7')
            return data

        else:
            return data
    else:
        if data['client']['phone'].isdigit() and not data['client']['phone'].startswith('8'):
            return data
        elif data['client']['phone'].startswith('+'):
            data['client']['phone'] = data['client']['phone'].replace('+', '')
            return data
        elif data['client']['phone'].startswith('8'):
            data['client']['phone'] = data['client']['phone'].replace('8', '7')
            return data
        else:
            return data

def fix_phone(data):
    phone = data['phone']
    if phone.isdigit() and not phone.startswith('8'):
        return data
    elif phone.startswith('+'):
        data['phone'] = phone.replace('+', '')
        return data
    elif phone.startswith('8'):
        data['phone'] = phone.replace('8', '7')
        return data
    else:
        return data
