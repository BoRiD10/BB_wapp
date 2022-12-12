import crm_integration.Adapter as Adapter
import crm_integration.Altegio as Altegio
import crm_integration.yclients as yclients


class Records:

    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_records[crm_data['name']]
        self.crm_data = crm_data
        self.Adapter = Adapter.Formatdata(self.crm_data).choise_adapt_class()

    # +
    def get_record(self, record_id='', client_id=None, short_link_token=False):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_record(record_id=record_id, client_id=client_id,
                                                         short_link_token=short_link_token)
        if 'errors' in first_data:
            return False

        # Передаем данные на адаптацию
        data = self.Adapter.record(first_data)
        # Validate
        return data

    # +
    def get_all_for_today(self):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_all_for_today()
        if 'errors' in first_data:
            return False
        # Передаем данные на адаптацию
        data = self.Adapter.records_today(first_data)
        # Validate
        return data

    # +
    def get_for_date(self, date):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_for_date(date)
        if 'errors' in first_data:
            return False
        # Передаем данные на адаптацию
        data = self.Adapter.records_today(first_data)
        # Validate
        return data

    # +
    def get_for_period(self, start_date='', end_date='', client_id=None, short_link_token=True):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_for_period(start_date=start_date, end_date=end_date,
                                                             client_id=client_id, short_link_token=short_link_token)

        if not first_data or 'errors' in first_data:
            return False
        # Передаем данные на адаптацию
        data = self.Adapter.records_today(first_data)
        # Validate
        return data

    def confirm(self, record_id, staff_id, services, client, datetime, seance_length, activity_id=0, save_if_busy=True, send_sms=False,
                attendance=2):
        first_data = self.pack(self.crm_data).confirm(record_id, staff_id, services, client, datetime, seance_length,
                                                      activity_id=activity_id, save_if_busy=save_if_busy, send_sms=send_sms,
                                                      attendance=attendance)

        if not first_data:
            return False

        data = self.Adapter.records_confirm(first_data)
        return data


class Clients:

    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_clients[crm_data['name']]
        self.crm_data = crm_data
        self.Adapter = Adapter.Formatdata(self.crm_data).choise_adapt_class()

    def get_by_id(self, client_id):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_by_id(client_id)
        # Передаем данные на адаптацию
        data = self.Adapter.clients_byid(first_data)
        # Validate
        return data

    def info_by_phone(self, phone):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_info_by_phone(phone)

        # Передаем данные на адаптацию
        data = self.Adapter.clients_byid(first_data)
        # Validate
        return data

    def all_with_birthdays_for_period(self, start_date, end_date=''):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_all_with_birthdays_for_period(start_date, end_date=end_date)
        # Передаем данные на адаптацию
        try:
            data = self.Adapter.birthdays_for_period_all(first_data)
        except:
            return first_data
        # Validate
        return data

    def get_all_clients_Base(self, request_phones):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_all_clients_base(request_phones)
        # Передаем данные на адаптацию
        data = self.Adapter.all_clients(first_data)
        # Validate
        return data

    def save_clients(self, add_params):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).save_clients(add_params)
        # Передаем данные на адаптацию
        data = self.Adapter.save_clients(first_data)
        # Validate
        return data


class Groups:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_groups[crm_data['name']]
        self.crm_data = crm_data
        self.Adapter = Adapter.Formatdata(self.crm_data).choise_adapt_class()

    def get_client_group_info(self, client_phone):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_client_group_info(client_phone)
        # Передаем данные на адаптацию
        data = self.Adapter.client_group_info(first_data)
        return data


class Staffs:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_clients[crm_data['name']]
        self.crm_data = crm_data

    # +
    def get_staff(self, staff=''):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_staff(staff=staff)
        # Передаем данные на адаптацию
        data = Adapter.Formatdata(self.crm_data).staff(first_data)
        # Validate
        return data


class Webhook:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_webhook[crm_data['name']]
        self.crm_data = crm_data

    def get_webhook_settings(self):
        data = self.pack(self.crm_data).get_webhook_settings()
        return data

    def post_webhook_settings(self, settings):
        data = self.pack(self.crm_data).post_webhook_settings(settings=settings)
        return data


class Loyaltys:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_loyaltys[crm_data['name']]
        self.crm_data = crm_data
        self.Adapter = Adapter.Formatdata(self.crm_data).choise_adapt_class()

    def get_cards_by_company_id(self):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_cards_by_company_id()
        # Сырые {"success":true,"data":[{"id":24794,"title":"Для клиентов маникюра","salon_group_id":66278,"salon_group":{"id":66278,"title":"Сеть Niki Nail"}}],"meta":[]}
        # Передаем данные на адаптацию
        data = self.Adapter.cards_by_company_id(first_data)
        # Validate
        return data

    def get_client_cards(self, client_id):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_client_cards(client_id)
        # Добавить обработку пустых данных по типу {"success":true,"data":[],"meta":[]}
        # Передаем данные на адаптацию
        data = self.Adapter.client_cards(first_data)
        # Validate
        return data

    def get_loyal_transactions_for_visit(self, visit_id):
        first_data = self.pack(self.crm_data).get_loyal_transactions_for_visit(visit_id)
        # Передаем данные на адаптацию
        data = self.Adapter.loyalty_transactions_Visit(first_data)
        # Validate
        return data

    def client_have_abonement(self, client_phone):
        first_data = self.pack(self.crm_data).client_have_abonement(client_phone)
        return first_data


class Service:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_service[crm_data['name']]
        self.crm_data = crm_data
        self.Adapter = Adapter.Formatdata(self.crm_data).choise_adapt_class()

    def get_all_branch_services(self):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_all_branch_services()
        if first_data is None:
            return None
        # Передаем данные на адаптацию
        data = self.Adapter.all_branch_services(first_data)
        # Validate
        return data

    def get_service_category(self, service_id):
        # Получаем сырые данные от API CRM
        first_data = self.pack(self.crm_data).get_service_category(service_id)
        # Передаем данные на адаптацию
        data = self.Adapter.service_category(first_data)
        # Validate
        return data


class Marketplace:
    def __init__(self, crm_data):
        # Определяем интеграцию
        self.pack = routing_marketplace[crm_data['name']]
        self.crm_data = crm_data

    def set_callback(self, acc_id):
        first_data = self.pack(self.crm_data).set_callback(acc_id)
        return first_data

    def payment(self, payment_sum, period_from, period_to):
        first_data = self.pack(self.crm_data).payment(payment_sum, period_from, period_to)
        return first_data

    def refund_payment(self, payment_id):
        first_data = self.pack(self.crm_data).refund_payment(payment_id)
        return first_data


routing_records = {'altegio': Altegio.Record, 'yclients': yclients.Record}
routing_clients = {'altegio': Altegio.Client, 'yclients': yclients.Client}
routing_loyaltys = {'altegio': Altegio.Loyalty, 'yclients': yclients.Loyalty}
routing_groups = {'altegio': Altegio.Group, 'yclients': yclients.Group}
routing_service = {'altegio': Altegio.Services, 'yclients': yclients.Services}
routing_webhook = {'yclients': yclients.Webhook, 'altegio': Altegio.Webhook}
routing_marketplace = {'yclients': yclients.Marketplace, 'altegio': Altegio.Marketplace}

# ================Tests============================
# crm_data = {'name': 'yclients', 'branch': '51696'}
# crm_data = {'name': 'altegio', 'branch': '305687'}
# now_msk = datetime.datetime.now()
# date = str(now_msk)[:10]

# print(Records(crm_data).get_record(record_id=463215729, short_link_token=True))
# print(Records(crm_data).get_all_for_today())
# print(Records(crm_data).get_for_date('2022-05-24'))
# print(Records(crm_data).get_for_period('2022-11-14', '2022-11-14', client_id=9881524))

# print(Clients(crm_data).get_by_id(145184745))
# print(Clients(crm_data).info_by_phone('79105775770'))
# print(Clients(crm_data).all_with_birthdays_for_period('2022-09-15', '2022-09-17'))
# print(Clients(crm_data).get_all_clients_Base([{'type': 'quick_search', 'state': {'value': '77084183839'}}]))
# print(Clients(crm_data).save_clients([{'name': 'Павлов Илья', 'phone': '79167848211'}, {'name': 'Павлов Илья', 'phone': '79167848212'}]))

# print(Staffs(crm_data).get_staff())

# print(Groups({'name': 'yclients', 'group_id': '69004'}).get_client_group_info('79067013265'))

# print(Loyaltys(crm_data).get_cards_by_company_id())
# pprint(Loyaltys(crm_data).get_loyal_transactions_for_visit(454849266))
# print(Loyaltys(crm_data).get_client_cards(145184745))
# print(Loyaltys(crm_data).client_have_abonement('79119905022'))

# print(Service(crm_data).get_all_branch_services())
# print(Service(crm_data).get_service_category(5233603))

# print(Webhook(crm_data).get_webhook_settings())

# moscow = pytz.timezone('Europe/Moscow')
# print(Marketplace(crm_data).payment(0, datetime.datetime.now(moscow), datetime.datetime.now(moscow) + datetime.timedelta(days=1)))
# print(Marketplace(crm_data).refund_payment(47614))
# =================================================
