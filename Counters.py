from pprint import pprint
from urllib.parse import urlencode, urljoin

import requests

AUTH_URL = "https://oauth.yandex.ru/authorize"
APP_ID = "db0de4066bde4910aef0a0b8b9052a81"

auth_data = {
    "response_type": "token",
    "client_id": APP_ID
}

# print("?".join((AUTH_URL, urlencode(auth_data))))
TOKEN = ""


class MetrikaBase:

    def __init__(self, token):
        self.__token = token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    def get_headers(self):
        return {
            "Authorization": "OAuth {}".format(self.token),
            "Content-Type": "application/x-yametrika+json"
        }


class MyMetrikaApp(MetrikaBase):

    MANAGEMENT_URL = "https://api-metrika.yandex.ru/management/v1/"

    def __init__(self, token):
        super().__init__(token)

    def get_headers(self):
        return {
            "Authorization": "OAuth {}".format(self.token),
            "Content-Type": "application/x-yametrika+json"
        }

    def get_counters(self):

        headers = self.get_headers()
        response = requests.get(urljoin(self.MANAGEMENT_URL, "counters"), headers=headers)

        return response.json()["counters"]

    def get_counter_info(self, counter_id):
        headers = self.get_headers()
        response = requests.get(urljoin(self.MANAGEMENT_URL, "counter/{}").format(counter_id), headers=headers)
        return response.json()["counter"]


class Counter(MetrikaBase):
    STAT_URL = "https://api-metrika.yandex.ru/stat/v1/data"

    def __init__(self, id, token):
        self.id = id
        super().__init__(token)

    def get_info(self, info):      # сделал один метод для всех метрик, исходя из того, что меняется только значение /
                                #  ключа "metrics" в словаре params.
        headers = self.get_headers()
        metric = ""
        params = {
            "id": self.id,
            "metrics": metric
        }
        if info == "visits":
            params["metrics"] = "ym:s:visits"
        elif info == "pageviews":
            params["metrics"] = "ym:pv:pageviews"
        elif info == "users":
            params["metrics"] = "ym:s:users"
        else:
            print("Invalid parameter")
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()

i_am_user = MyMetrikaApp(TOKEN)
counters = i_am_user.get_counters()

for c in counters:
    counter = Counter(c["id"], TOKEN)
    param = input("Введите параметр:\n"
                  "pageviews - просмотры\n"
                  "users - посетители\n"
                  "visits - визиты\n"
                  )
pprint(counter.get_info(param))


