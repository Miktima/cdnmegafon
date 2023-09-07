import requests
from datetime import date
from django.conf import settings

class Statsite:
    def __init__(self):
    # Определяем параметры запросов
        self.service = "?service=CDN"
        self.fromdate = "&from="
        self.todate = "&to="
        self.granulaValue = "&granularity="
        self.metric = "&metrics="
        self.groupby = "&group_by=resource"
        self.resource = "&resource="
        # Результирующее число точек, которое определятся как разница между from/to деленое на granularity не должно превышать 1440.
        self.max_point = 1440
        # Возможная гранулярность
        self.gran = {
            60: "1m",
            300: "5m",
            900: "15m",
            3600: "1h",
            86400: "1d"
        }        

    def granula(self, tfrom:date, tto:date):
        # Определяется параметр granularity
        dift = tto - tfrom
        difsec = dift.total_seconds()
        # Прибавляем секунды за одни сутки
        difsec += 3600 * 24
        gran_seconds = self.gran.keys()
        choose_gran = False
        result = ""
        for sec in gran_seconds:
            if (difsec/sec) <= self.max_point:
                choose_gran = True
                result = self.gran.get(sec)
                return result
        # Проверка, что максимальное разбиение не будет превышать допустимое
        if choose_gran == False and (difsec/gran_seconds[len(gran_seconds) - 1]) > self.max_point:
            self.error = "Too large range between from and to dates (" + str(difsec) + " seconds)"
            return False
        else:
            result = self.gran.get(gran_seconds[len(gran_seconds) - 1])
            return result

    def get_stat(self, portal_id, date_from:date, date_to:date, metric):
        # получаем статистику за указанный период
        if self.granula(date_from, date_to) != False:
            granula = self.granula(date_from, date_to)
        else:
            return False
        request = self.service + self.fromdate + date_from.isoformat() + "T00:00:00Z" \
                    + self.todate + date_to.isoformat() + "T23:59:59Z" \
                    + self.granulaValue + granula + self.metric + metric + self.groupby \
                    + self.resource + portal_id
        headers = {'Authorization': 'APIKey ' + settings.APIKEY}
        response = requests.get(settings.APIURLS['urlResStat'] + request, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print ("Request URL: ", response.url)
            print ("ERROR: code - ", response.status_code)
            return False
    