from datetime import datetime
from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


class MetricPlot:
    def __init__(self):
    # Определяем константы
        self.gbyte = 1024 * 1024 * 1024
        self.mil = 1000000


    def StatPlot(self, metric, portal_id, response):
        # Проверяем, что метрика должна возвращать байты и определяем заголовок графика
        match metric:
            case 'upstream_bytes':
                title = 'Traffic from the source to the CDN servers'
                factor = self.gbyte
                ylable = 'GB'
            case 'sent_bytes':
                title = 'Traffic from CDN servers to the end users'
                factor = self.gbyte
                ylable = 'GB'
            case 'shield_bytes':
                title = 'Traffic from shielding to CDN servers'
                factor = self.gbyte
                ylable = 'GB'
            case 'total_bytes':
                title = 'The sum of shield_bytes, upstream_bytes and sent_bytes traffic'
                factor = self.gbyte
                ylable = 'GB'
            case 'cdn_bytes':
                title = 'The sum of sent_bytes and shield_bytes traffic'
                factor = self.gbyte
                ylable = 'GB'
            case 'requests':
                title = 'The number of requests to the CDN servers'
                factor = self.mil
                ylable = 'Million'
            case 'requests_waf_passed':
                title = 'The number of requests that were processed by the Basic WAF option'
                factor = self.mil
                ylable = 'Million'
            case 'responses_2xx':
                title = 'The number of 2xx HTTP response status codes'
                factor = self.mil
                ylable = 'Million'
            case 'responses_3xx':
                title = 'The number of 3xx HTTP response status codes'
                factor = self.mil
                ylable = 'Million'
            case 'responses_4xx':
                title = 'The number of 4xx HTTP response status codes'
                factor = self.mil
                ylable = 'Million'
            case 'responses_5xx':
                title = 'The number of 5xx HTTP response status codes'
                factor = self.mil
                ylable = 'Million'
            case 'responses_hit':
                title = 'The number of responses with the HTTP header Cache: HIT'
                factor = self.mil
                ylable = 'Million'
            case 'responses_miss':
                title = 'The number of responses with the HTTP header Cache: MISS'
                factor = self.mil
                ylable = 'Million'
            case 'image_processed':
                title = 'The number of images processed by the Image optimization option'
                factor = self.mil
                ylable = 'Million'
            case 'cache_hit_traffic_ratio':
                title = 'The amount of cached traffic'
                factor = 1
                ylable = 'Ratio'
            case 'cache_hit_requests_ratio':
                title = 'The amount of cached content that is sent'
                factor = 1
                ylable = 'Ratio'
            case 'shield_traffic_ratio':
                title = 'The efficiency of shielding'
                factor = 1
                ylable = 'Ratio'
            case _:
                print ("ERROR: unsupported metric for StatPlot")
                return False
        # Добираемся до данных формата: 
        # 1680570000 — the time in the UNIX timestamp at which the statistics were received
        # 17329220573 — number of bytes
        data = response['resource'][portal_id]['metrics'][metric]
        plot_y = []
        plot_x = []
        for value in data:
            # переводим в миллионы
            plot_y.append(value[1]/factor)
            # переводим в питоновские объекты
            plot_x.append(datetime.fromtimestamp(value[0]))
        # Определение тиков для оси ординат (дат)
        locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
        formatter = mdates.ConciseDateFormatter(locator)
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(plot_x, plot_y)
        ax.set_title(title) 
        plt.plot(plot_x, plot_y)
        plt.ylabel(ylable)
        plt.autoscale()
        # График сохраняем в памяти и передаем в шаблон
        img_in_memory = BytesIO()
        plt.savefig(img_in_memory, format="png")
        data_plot = base64.b64encode(img_in_memory.getvalue()).decode()
        plt.clf()
        return data_plot        

