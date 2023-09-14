from datetime import datetime
from io import BytesIO
import base64
import pandas as pd

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

class LogConstruct:
    def __init__(self):
    # Определяем параметры запроса
        self.limit = "?limit=1000"
        self.fromdate = "&from="
        self.todate = "&to="
        self.resource = "&resource_id__eq="
    # Заголовки графиков
        self.plot_titiles = {
            'path': 'The requested path',
            'user_agent': 'The User-Agent HTTP header value',
            'method': 'HTTP method used in the request',
            'client_ip': 'The IP from which the request was made',
            'status': 'HTTP status code',
            'size': 'Response size in bytes',
            'cache_status': 'The cache status',
            'datacenter': 'The data center where the request was processed'
        }

    def consructRequest(self, resource_id, filters, fromdate:datetime, todate:datetime):
        # формат для даты - (ISO 8086/RFC 3339 format; UTC)
        req = self.limit + self.resource + resource_id + self.fromdate + fromdate.isoformat() + "Z" \
                + self.todate + todate.isoformat() + "Z"
        for f in filters:
            req += "&" + f["filter"] + "__" + f["operator"] + "=" + f["value"]
            if f["value2"] != "":
                req += "&" + f["filter"] + "__" + f["operator2"] + "=" + f["value2"]
        return req
    
    def logPlot(self, data, aggregate:list):
        # Проверяем, что метрика должна возвращать байты и определяем заголовок графика
        log_table = pd.DataFrame.from_records(data)
        x=[]
        xticks = []
        for i in range(1,21):
            x.append(i)
            if (i%4) == 0:
                xticks.append(i)
        data = []
        for agg in aggregate:
            tmpDict = {}
            # request_uri chart
            ser = (log_table[agg].value_counts()).head(20)
            tmpDict["values"] = ser.to_dict()
            # x_values = ser.tolist()
            fig, ax = plt.subplots(figsize=(7, 7))
            ax.bar(x, ser, width=1, edgecolor="white", linewidth=0.7, align='edge')
            ax.set(xlim=(1, 20), xticks=xticks)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.set_title(self.plot_titiles[agg]) 
            tmpDict["title"] = self.plot_titiles[agg]
            img = BytesIO()
            plt.savefig(img, format="png")
            tmpDict["plot"] = base64.b64encode(img.getvalue()).decode()
            plt.clf()
            data.append(tmpDict)
        return data        