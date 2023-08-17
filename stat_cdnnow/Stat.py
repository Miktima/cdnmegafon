import requests
import json
from .models import Stat_settings

class Statsite:
    def __init__(self):
    # Определяем параметры запросов
        settings = Stat_settings.objects.first()
        self.login = settings.login
        self.password = settings.password
        self.id_client = settings.client_id
        self.cdnnow_urlauth = settings.url_auth
        self.cdnnow_urlstat = settings.url_stat
        
    def get_token(self):
        # Получаем токен для последующих запросов
        login_data = {
            'username': self.login,
            'password': self.password
        }
        response = requests.post(self.cdnnow_urlauth, data = login_data)
        if (response.json())["status"] != "ok":
            print ("ERROR: response status:", response.json())
            return False
        else:
            data = (response.json())["data"]
            return data["token"]
    
    def get_stat(self, token, id_portal, stat_period:list):
        # получаем статистику за день, если указан день, или за месяц, если день не указан
        request_data = {
            "token": token,
            "year": stat_period[0],
            "month": stat_period[1],
            "client": self.id_client,
            "project": id_portal
        }
        if stat_period[2] != "":
            request_data.update({"day": stat_period[2]})
        response = requests.get(self.cdnnow_urlstat, params = request_data)
        if response.status_code == 200:
            return (response.json())["data"]["data"]
        else:
            print ("Request URL: ", response.url)
            print ("ERROR: code - ", response.status_code)
            return False
    