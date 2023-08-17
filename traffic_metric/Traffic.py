import requests
from datetime import date
from .models import Granularity, Metric_settings, Metrics

class Trafficsite:
    def __init__(self):
        # Результирующее число точек, которое определятся как разница между from/to деленое на granularity не должно превышать 1440.
        self.max_point = 1440
        granula_list = Granularity.objects.all().order_by('nsec') 
        self.gran = {}
        for g in granula_list:
            self.gran.update({g.nsec:g.code})
        self.filter_by =[{
            "field": "cname", 
            "op": "in", 
            "values": "userXXXXX"
        }]
        self.group_by = ["cname"]
        metrics_obj = Metrics.objects.all()
        self.metrics = []
        for m in metrics_obj:
            self.metrics.append(m.name)
        settings = Metric_settings.objects.first()
        self.cdnnow_url = settings.url_metric
        self.token = settings.token
        self.error = ""

    def granula(self, tfrom:date, tto:date, param=True):
        # Определяется параметр granularity
        dift = tto - tfrom
        difsec = dift.total_seconds()
        # Если параметр True прибавляем секунды за одни сутки
        if param == True:
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

    def get_traffic_metric(self, project, date_from:date, date_to:date):
        if self.granula(date_from, date_to) != False:
            granula = self.granula(date_from, date_to)
        else:
            return False
        ((self.filter_by)[0]).update({"values": [project]})
        request_data = {
            "metrics": self.metrics,
            "from": date_from.isoformat() + "T00:00:00Z",
            "to": date_to.isoformat() + "T23:59:59Z",
            "granularity": granula,
            "filter_by": self.filter_by,
            "group_by": self.group_by
        }
        response = requests.post(self.cdnnow_url, headers={"x-auth-token": self.token}, json=request_data)
        if response.status_code == 200:
            return (response.json())["data"][project]
        else:
            self.error = "ERROR: code - ", response.status_code, " ", response.text
            return False
    