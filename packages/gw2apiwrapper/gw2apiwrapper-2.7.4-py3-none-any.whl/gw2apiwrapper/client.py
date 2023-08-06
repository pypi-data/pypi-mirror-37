from gw2apiwrapper import AccountAPI, GlobalAPI


class Client(GlobalAPI):
    def __init__(self, apikey=None):
        # self.url = 'https://api.guildwars2.com/v2/'
        # self.__dict__ = GlobalAPI().__dict__
        self.__dict__.update(GlobalAPI().__dict__)

        if apikey:
            self.authed = AccountAPI(apikey)
