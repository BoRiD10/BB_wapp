from wapp_logic import Adapter
import wapp_logic.green_api as gp
import wapp_logic.wappi as wp
from configs import config, config_beauty


class Wapp:

    def __init__(self, chat_api_data):
        if 'green-api' in chat_api_data['url']:
            name = 'green-api'
        else:
            name = 'wappi'
        self.pack = routng_wapp[name]
        self.chat_api_data = chat_api_data
        self.Adapter = Adapter.FormatData(self.chat_api_data).choose_adapt_class()

    def set_settings(self, state=False):
        first_data = self.pack(self.chat_api_data).set_settings(state=state)
        data = self.Adapter.set_settings(first_data)
        return data


routng_wapp = {'green-api': gp.Green_Api, 'https://green-api/': gp.Green_Api, 'wappi': wp.Wappi}


