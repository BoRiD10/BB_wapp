from crm_integration.schemas import ClearDate
from crm_integration.utilities import fix_number, end_time_delta, fix_utc_date, fix_data_phone_in_loop, fix_phone


class AltegioForms:
    # Приводим сырые данные altegio к внутреней форме
    def record(self, first_data):
        first_data['name'] = 'altegio'
        first_data = fix_number(first_data)
        first_data = fix_utc_date(first_data)
        first_data = end_time_delta(first_data)
        data = ClearDate.clear_record(first_data)
        return data

    def records_today(self, first_data):
        """
        Works with get_record(), get_all_for_today(), get_for_date(),
        get_for_period(), get_for_period_DL()
        :param first_data:
        :return: clear dict
        """
        crm_name = 'altegio'
        first_data['data'] = fix_data_phone_in_loop(first_data, crm_name)
        data = ClearDate.clear_today(first_data)
        return data

    def records_confirm(self, first_data):
        data = ClearDate.clear_confirm(first_data)
        return data

    def clients_byid(self, first_data):
        """
        Works with get_by_id(), get_id_by_phone(), get_info_by_phone(),
        :param first_data:
        :return: clear dict
        """
        first_data = fix_phone(first_data)
        data = ClearDate.clear_byid(first_data)
        return data

    def staff(self, first_data):
        """
        Works with get_staff()
        :param first_data:
        :return: clear dict
        """
        if type(first_data['data']) is dict:
            first_data['data'] = [first_data['data']]
        first_data['total_count'] = len(first_data['data'])
        data = ClearDate.clear_staff(first_data)
        return data

    def birthdays_for_period_all(self, first_data):
        """
        Works with get_all_with_birthdays_for_period()
        :param first_data:
        :return: clear dict
        """
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count
        first_data['data'] = list(map(lambda cl_data: fix_phone(cl_data), first_data['data']))
        data = ClearDate.clear_birth_days(first_data)
        return data

    def all_clients(self, first_data):
        data = ClearDate.clear_all_clients(first_data)
        return data

    def client_group_info(self, first_data):
        """
        Works with get_client_group_info()
        :param first_data:
        :return: clear dict
        """
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count

        data = {'data': ClearDate.clear_group_info(first_data['data'])}
        return data

    def cards_by_company_id(self, first_data):
        """
        Works with get_cards_by_company_id()
        :param first_data:
        :return: clear dict
        """
        data = ClearDate.clear_loyalty_cards_company(first_data)
        return data

    def client_cards(self, first_data):
        """
        Works with get_client_cards()
        :param first_data:
        :return: clear dict
        """
        if not first_data['data']:
            return {'data': []}

        data = ClearDate.clear_loyalty_cards_client(first_data)
        return data

    def all_branch_services(self, first_data):
        """
        Works with get_all_branch_services()
        :param first_data:
        :return: clear dict
        """
        first_data['name'] = 'altegio'
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count

        data = ClearDate.clear_services_branch(first_data)
        return data

    def service_category(self, first_data):
        """
        Works with get_service_category()
        :param first_data:
        :return: clear dict
        """
        first_data['name'] = 'altegio'
        data = ClearDate.clear_category_service(first_data)
        return data

    def loyalty_client_abonement(self, first_data):
        data = ClearDate.clear_loyalty_client_abonemen(first_data)
        return data

    def loyalty_transactions_Visit(self, first_data):

        data = ClearDate.clear_loyalty_Transactions_Visit(first_data)
        return data


class YclientsForms:
    # Приводим сырые данные ycl к внутреней форме
    def record(self, first_data):
        first_data['name'] = 'yclients'
        first_data = fix_number(first_data)
        first_data = fix_utc_date(first_data)
        first_data = end_time_delta(first_data)
        data = ClearDate.clear_record(first_data)
        return data

    def records_today(self, first_data):
        """
        Works with get_record(), get_all_for_today(), get_for_date(), get_for_period()
        :param first_data:
        :return: clear dict
        """
        crm_name = 'yclients'
        first_data['data'] = fix_data_phone_in_loop(first_data, crm_name)
        data = ClearDate.clear_today(first_data)
        return data

    def records_confirm(self, first_data):
        data = ClearDate.clear_confirm(first_data)
        return data

    def clients_byid(self, first_data):
        """
        Works with get_by_id(), get_id_by_phone(), get_info_by_phone(),
        :param first_data:
        :return: clear dict
        """
        first_data = fix_phone(first_data)
        data = ClearDate.clear_byid(first_data)
        return data

    def all_clients(self, first_data):
        data = ClearDate.clear_all_clients(first_data)
        return data

    def save_clients(self, first_data):
        data = ClearDate.clear_clients_save(first_data)
        return data

    def staff(self, first_data):
        """
        Works with get_staff()
        :param first_data:
        :return: clear dict
        """
        if type(first_data['data']) is dict:
            first_data['data'] = [first_data['data']]
        first_data['total_count'] = len(first_data['data'])
        data = ClearDate.clear_staff(first_data)
        return data

    def birthdays_for_period_all(self, first_data):
        """
        Works with get_all_with_birthdays_for_period()
        :param first_data:
        :return: clear dict
        """
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count
        first_data['data'] = list(map(lambda cl_data: fix_phone(cl_data), first_data['data']))
        data = ClearDate.clear_birth_days(first_data)
        return data

    def client_group_info(self, first_data):
        """
        Works with get_client_group_info()
        :param first_data:
        :return: clear dict
        """
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count

        data = {'data': ClearDate.clear_group_info(first_data['data'])}
        return data

    def cards_by_company_id(self, first_data):
        """
        Works with get_cards_by_company_id()
        :param first_data:
        :return: clear dict
        """
        data = ClearDate.clear_loyalty_cards_company(first_data)
        return data

    def client_cards(self, first_data):
        """
        Works with get_client_cards()
        :param first_data:
        :return: clear dict
        """
        data = ClearDate.clear_loyalty_cards_client(first_data)
        return data

    def all_branch_services(self, first_data):
        """
        Works with get_all_branch_services()
        :param first_data:
        :return: clear dict
        """
        first_data['name'] = 'yclients'
        total_count = len(first_data['data'])
        first_data['total_count'] = total_count

        data = ClearDate.clear_services_branch(first_data)
        return data

    def service_category(self, first_data):
        """
        Works with get_service_category()
        :param first_data:
        :return: clear dict
        """
        first_data['name'] = 'yclients'
        data = ClearDate.clear_category_service(first_data)
        return data

    def loyalty_client_abonemen(self, first_data):
        data = ClearDate.clear_loyalty_client_abonemen(first_data)
        return data

    def loyalty_transactions_Visit(self, first_data):
        data = ClearDate.clear_loyalty_Transactions_Visit(first_data)
        return data


class Formatdata(AltegioForms, YclientsForms):

    def __init__(self, crm_data):
        self.crm_data = crm_data
        if crm_data['name'] == 'yclients':
            self.crm = YclientsForms
        elif crm_data['name'] == 'altegio':
            self.crm = AltegioForms

    def choise_adapt_class(self):
        return self.crm()
