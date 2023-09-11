from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pandas as pd
from io import BytesIO
import base64
from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from django.conf import settings
import requests

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


def index(request):
    # Заполняем список проектов (порталов), для работы с API используется имя портала
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
    # Заполняем списки для дат
    years = [2021, 2022, 2023]
    months = []
    for i in range (1, 13):
        months.append(i)
    days = []
    for i in range (1, 32):
        days.append(i)
    hours = []
    for i in range (0, 24):
        hours.append(i)
    minutes = []
    for i in range (0, 60):
        minutes.append(i)
    td = datetime.today()
    current_year = int(td.strftime("%Y"))
    current_month = int(td.strftime("%m"))
    current_day = int(td.strftime("%d"))
    context = {
        'portal_list': portal_list,
        'years': years,
        'months': months,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'current_year': current_year,
        'current_month': current_month,
        'current_day': current_day,
        'logfilter': settings.LOGFILTER,
        'logoperator': settings.LOGOPERATOR,
        'logoperatorplus': settings.LOGOPERATORPLUS,
        'logmethod': settings.LOGMETHOD,
        'logcachestatus': settings.LOGCACHESTATUS
    }
    return render(request, "log_analyse/index.html", context)

def results(request):
    portal_id = request.POST['portal']
    if portal_id == 'no_select':
        messages.error(request, 'Требуется выбрать портал')
        return HttpResponseRedirect(reverse('metric_index'))       
    # Формируем начальную и конечную дату получения метрик
    from_date = datetime(int(request.POST['from_year']), int(request.POST['from_month']), \
                        int(request.POST['from_day']), int(request.POST['from_hour']), \
                        int(request.POST['from_min']) )
    # Для получения конечной даты прибавляем 6 часов
    to_date = from_date + timedelta(hours = 6)
    metrics_list = request.POST.getlist('metrics')
    if len(metrics_list) == 0:
        messages.error(request, 'Хотя бы одна метрика должна быть выбрана')
        return HttpResponseRedirect(reverse('metric_index'))            
    # Формируем начальную и конечную дату получения метрик
    # Для начальной даты время идет с 0 часов, для конечной даты время устанавливается 23-59
    from_date = date(int(request.POST['from_year']), int(request.POST['from_month']), int(request.POST['from_day']))
    to_date = date(int(request.POST['to_year']), int(request.POST['to_month']), int(request.POST['to_day']))
    # Проверка, что начальная дата должна быть меньше конечной
    if from_date > to_date:
        messages.error(request, 'Дата начала периода должна быть меньше даты окончания')
        return HttpResponseRedirect(reverse('metric_index'))        
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

