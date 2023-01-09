from typing import List, Optional

from pydantic import BaseModel, ValidationError


class InstanceDataModel(BaseModel):
    idInstance: str


class WappiAuthHookModel(BaseModel):
    instanceData: InstanceDataModel
    stateInstance: str


class StandartHookModel(BaseModel):
    body: str
    id: str
    from_me: bool
    is_forwarded: bool
    time: str
    chat_id: str
    phone: str
    type: str
    sender_name: str
    channel: str
    message_id: str
    cached: bool
    caption: Optional[str]


class SetSettingsModel(BaseModel):
    saveSettings: bool


class ClearData:

    @classmethod
    def clear_wappi_auth_hook(cls, first_data):
        try:
            clear_wappi_auth_hook = WappiAuthHookModel.parse_obj(first_data)
            return clear_wappi_auth_hook.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_standart_hook(cls, first_data):
        try:
            clear_standart_hook = StandartHookModel.parse_obj(first_data)
            return clear_standart_hook.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'

    @classmethod
    def clear_set_settings(cls, first_data):
        try:
            clear_settings = SetSettingsModel.parse_obj(first_data)
            return clear_settings.dict()
        except ValidationError as e:
            return f'Exception {e.json()}'
