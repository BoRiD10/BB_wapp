from typing import List

from pydantic import BaseModel, ValidationError
from pydantic.datetime_parse import datetime


class RecordClient(BaseModel):
    id: int
    name: str
    phone: str
    success_visits_count: int
    fail_visits_count: int


class RecordStaff(BaseModel):
    id: int
    name: str


class RecordGoodsTransactions(BaseModel):
    id: int
    title: str
    article: str
    amount: int
    cost_per_unit: int
    cost: int
    master_id: int
    storage_id: int
    good_id: int


class RecordServices(BaseModel):
    id: int
    title: str
    cost: int
    cost_per_unit: int
    first_cost: int
    amount: int


class RecordDataBase(BaseModel):
    name: str
    id: int
    company_id: int
    services: List[RecordServices] = None
    goods_transactions: List[RecordGoodsTransactions]
    staff: RecordStaff
    client: RecordClient = None
    clients_count: int
    datetime: datetime
    create_date: datetime
    online: bool
    attendance: int
    confirmed: int
    seance_length: int
    length: int
    master_request: int
    visit_id: int
    created_user_id: int
    deleted: bool
    paid_full: int
    last_change_date: datetime
    end_time: datetime
    short_link_token: str = None
    date: str = None


class RecordClientOther(BaseModel):
    id: int
    name: str
    phone: str
    success_visits_count: int
    fail_visits_count: int


class RecordStaffOther(BaseModel):
    id: int
    name: str


class RecordGoodsTransactionsOther(BaseModel):
    id: int
    title: str
    article: str
    amount: int
    cost_per_unit: int
    cost: int
    master_id: int
    storage_id: int
    good_id: int


class RecordServicesOther(BaseModel):
    id: int
    title: str
    cost: int
    cost_per_unit: int
    first_cost: int
    amount: int


class RecordDataOther(BaseModel):
    name: str
    id: int
    company_id: int
    services: List[RecordServices] = None
    goods_transactions: List[RecordGoodsTransactions]
    staff: RecordStaff
    client: RecordClient = None
    clients_count: int
    datetime: datetime
    create_date: datetime
    online: bool
    attendance: int
    confirmed: int
    seance_length: int
    length: int
    master_request: int
    visit_id: int
    created_user_id: int
    deleted: bool
    paid_full: int
    last_change_date: datetime
    end_time: datetime
    short_link_token: str = None
    date: str = None
    activity_id: int


class RecordBaseDataOther(BaseModel):
    data: List[RecordDataOther]


class ByIdCategories(BaseModel):
    id: int
    title: str
    color: str


class ByIdBase(BaseModel):
    id: int
    name: str
    phone: str
    birth_date: str
    visits: int
    sex: str = None
    spent: int
    importance_id: int
    categories: List[ByIdCategories]
    last_change_date: datetime


class BirthdaysData(BaseModel):
    id: int
    phone: str
    name: str
    visits_count: int


class BirthdaysBase(BaseModel):
    success: bool
    total_count: int
    data: List[BirthdaysData]


class GroupInfoClients(BaseModel):
    id: int
    company_id: int
    name: str


class GroupInfoBase(BaseModel):
    salon_group_id: int
    phone: str
    clients: List[GroupInfoClients]


class LoyaltyCardsCompanySalonGroup(BaseModel):
    id: int
    title: str


class LoyaltyCardsCompanyBase(BaseModel):
    id: int
    title: str
    salon_group_id: int
    salon_group: LoyaltyCardsCompanySalonGroup


class LoyaltyCards(BaseModel):
    data: List[LoyaltyCardsCompanyBase]


class LoyaltyCardsClientSalonGroup(BaseModel):
    id: int
    title: str


class LoyaltyCardsClientType(BaseModel):
    id: int
    title: str
    salon_group_id: str


class LoyaltyCardsClientData(BaseModel):
    id: int
    balance: float
    points: int
    paid_amount: int
    sold_amount: int
    visits_count: int
    number: str
    type_id: int
    type: LoyaltyCardsClientType
    salon_group: LoyaltyCardsClientSalonGroup


class LoyaltyCardsClientBase(BaseModel):
    data: List[LoyaltyCardsClientData]


class LoyaltyTransactionsVisitProgram(BaseModel):
    id: int
    title: str
    value: int
    loyalty_type_id: int


class LoyaltyTransactionsVisitType(BaseModel):
    id: int
    title: str


class LoyaltyTransactionsVisitData(BaseModel):
    id: int
    card_id: int
    amount: int
    salon_group_id: int
    is_discount: bool
    is_loyalty_withdraw: bool
    type: LoyaltyTransactionsVisitType
    program: LoyaltyTransactionsVisitProgram


class LoyaltyTransactionsVisitBase(BaseModel):
    data: List[LoyaltyTransactionsVisitData]


class LoyaltyClientAbonementCount(BaseModel):
    count: bool


class LoyaltyClientAbonementBase(BaseModel):
    meta: List[LoyaltyClientAbonementCount]


class ServicesBranchData(BaseModel):
    id: int
    category_id: int


class ServicesBranchBase(BaseModel):
    name: str
    total_count: int
    data: List[ServicesBranchData]


class ServicesCategoryData(BaseModel):
    id: int
    category_id: int


class ServicesCategoryBase(BaseModel):
    name: str
    data: ServicesCategoryData


class StaffData(BaseModel):
    id: int
    name: str
    company_id: int
    specialization: str
    fired: bool
    status: bool
    hidden: bool


class StaffBase(BaseModel):
    total_count: int
    success: bool
    data: List[StaffData]


class ConfirmClient(BaseModel):
    phone: str
    name: str


class ConfirmServices(BaseModel):
    id: int
    cost: int


class ConfirmBase(BaseModel):
    staff_id: int
    services: List[ConfirmServices]
    client: ConfirmClient
    datetime: datetime
    seance_length: int
    attendance: int


class ClientsSaveBase(BaseModel):
    success: bool


class ClientsSaveAll(BaseModel):
    name: str
    id: int


class ClientsSaveAllBase(BaseModel):
    success: bool
    data: List[ClientsSaveAll]


# =========================================


class ClearDate:

    @classmethod
    def clear_loyalty_client_abonemen(cls, dirt_json):
        """
        Works with get_record()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = LoyaltyClientAbonementBase.parse_raw(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_record(cls, dirt_json):
        """
        Works with get_record()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = RecordDataBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_today(cls, dirt_json):
        """
        Works with get_record(), get_all_for_today(), get_for_date(),
        get_for_period(), get_for_period_DL()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = RecordBaseDataOther.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_loyalty_Transactions_Visit(cls, dirt_json):
        """
             Works with save_clients(self, params)
             :param dirt_json:
             :return: clear dict
             """
        try:
            t = LoyaltyTransactionsVisitBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_all_clients(cls, dirt_json):
        """
             Works with save_clients(self, params)
             :param dirt_json:
             :return: clear dict
             """
        try:
            t = ClientsSaveAllBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_clients_save(cls, dirt_json):
        """
             Works with save_clients(self, params)
             :param dirt_json:
             :return: clear dict
             """
        try:
            t = ClientsSaveBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_confirm(cls, dirt_json):
        """
             Works with confirm()
             :param dirt_json:
             :return: clear dict
             """
        try:
            t = ConfirmBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_staff(cls, dirt_json):
        """
        Works with get_staff()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = StaffBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_category_service(cls, dirt_json):
        """
        Works with get_service_category()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = ServicesCategoryBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_services_branch(cls, dirt_json):
        """
        Works with get_all_branch_services()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = ServicesBranchBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_loyalty_cards_client(cls, dirt_json):
        """
        Works with get_client_cards()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = LoyaltyCardsClientBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_loyalty_cards_company(cls, dirt_json):
        """
        Works with
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = LoyaltyCards.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_group_info(cls, dirt_json):
        """
        Works with get_client_group_info()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = GroupInfoBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_byid(cls, dirt_json):
        """
        Works with get_by_id(), get_id_by_phone(), get_info_by_phone(),
        :param dirt_json:
        :return: clear dict
        """

        try:
            t = ByIdBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_birth_days(cls, dirt_json):
        """
        Works with get_all_with_birthdays_for_period()
        :param dirt_json:
        :return: clear dict
        """
        try:
            t = BirthdaysBase.parse_obj(dirt_json)
            return t.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'
