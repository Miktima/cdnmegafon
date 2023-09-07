from django.shortcuts import render
from datetime import date
from datetime import datetime
from .Stat import Statsite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
import requests

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

def index(request):
    # Выбираем список ресурсов
    headers = {'Authorization': 'APIKey ' + settings.APIKEY}
    # Выборка ресурсов
    resources = requests.get(settings.APIURLS['urlResources'], headers=headers)
    status_code = resources.status_code
    if status_code != 200:
        messages.error(request, "Ошибка выборки порталов: " + status_code)
    res = resources.json()
    portal_list = []
    for r in res:
        resDict = {}
        resDict["id"] = r["id"]
        resDict["description"] = r["description"]
        portal_list.append(resDict)
    # Заполняем списки для выбора даты
    years = [2021, 2022, 2023]
    months = []
    for i in range (1, 13):
        months.append(i)
    days = []
    for i in range (1, 32):
        days.append(i)
    td = date.today()
    current_year = int(td.strftime("%Y"))
    current_month = int(td.strftime("%m"))
    current_day = int(td.strftime("%d"))
    context = {
        'portal_list': portal_list,
        'years': years,
        'months': months,
        'days': days,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day
    }
    return render(request, "stat_cdn/index.html", context)

def results(request):
    portal_id = request.POST['portal']
    if portal_id == 'no_select':
        messages.error(request, 'Необходимо выбрать портал')
        return HttpResponseRedirect(reverse('stat_index'))
    objStat = Statsite()
    # Формируем начальную и конечную дату получения метрик
    # Для начальной даты время идет с 0 часов, для конечной даты время устанавливается 23-59
    from_date = date(int(request.POST['from_year']), int(request.POST['from_month']), int(request.POST['from_day']))
    to_date = date(int(request.POST['to_year']), int(request.POST['to_month']), int(request.POST['to_day']))
    # Проверка, что начальная дата должна быть меньше конечной
    if from_date > to_date:
        messages.error(request, 'Дата начала периода должна быть меньше даты окончания')
        return HttpResponseRedirect(reverse('stat_index'))
    # Вытаскиваем CDN портала
    headers = {'Authorization': 'APIKey ' + settings.APIKEY}
    # Выборка ресурсов
    resources = requests.get(settings.APIURLS['urlResources'] + "/" + portal_id, headers=headers)
    status_code = resources.status_code
    if status_code != 200:
        messages.error(request, "Ошибка выборки портала: " + str(status_code))
    res = resources.json()
    portal = res["cname"]
    if len(res["secondaryHostnames"]) > 0:
        for secCname in res["secondaryHostnames"]:
            portal += "; " + secCname
    # Отправляем запрос на метрику sent_bytes - to get traffic in bytes from CDN servers to the end users   
    responce = objStat.get_stat(portal_id, from_date, to_date, "sent_bytes")
    # Если ответ положительный готовим данные для вывода на график
    if responce != False:
        # Добираемся до данных формата: 
        # 1680570000 — the time in the UNIX timestamp at which the statistics were received
        # 17329220573 — number of bytes
        data = responce['resource'][portal_id]['metrics']['sent_bytes']
        plot_y = []
        plot_x = []
        for value in data:
            # переводим в Гигабайты
            plot_y.append(value[1]/1024/1024/1024)
            # переводим в питоновские объекты
            plot_x.append(datetime.fromtimestamp(value[0]))
        # Определение тиков для оси ординат (дат)
        locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
        formatter = mdates.ConciseDateFormatter(locator)
        fig, ax = plt.subplots(figsize=(7, 7), layout='constrained')
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(plot_x, plot_y)
        ax.set_title("Edge cache status hit ratio") 
        plt.plot(plot_x, plot_y)
        plt.ylabel('GB')
        plt.autoscale()
        # График сохраняем в памяти и передаем в шаблон
        img_in_memory = BytesIO()
        plt.savefig(img_in_memory, format="png")
        data_plot = base64.b64encode(img_in_memory.getvalue()).decode()
        plt.clf()
# Форматирование вывода периода для шаблона
    period = request.POST['from_day'] + "/" + request.POST['from_month'] + "/" \
            + request.POST['from_year'] + " - " + request.POST['to_day'] + "/" \
            + request.POST['to_month'] + "/" + request.POST['to_year']
    context = {
        "portal": portal,
        "plot": data_plot,
        "period": period
    }
    return render(request, 'stat_cdn/results.html', context)