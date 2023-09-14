from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib import messages
from datetime import datetime
from datetime import timedelta
from django.conf import settings
import requests
from .LogConstruct import LogConstruct

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
    if request.method == "POST":
        headers = {'Authorization': 'APIKey ' + settings.APIKEY}
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
        # Формируем список фильтров и фильтров для построения графиков
        filter_list = []
        filter_plot = []
        for filter in settings.LOGFILTER:
            tmpFilter = {}
            if (request.POST[filter + '_value'] == 'no' or request.POST[filter + '_value'] == '') == False:
                tmpFilter["filter"] = filter
                tmpFilter["value"] = request.POST[filter + '_value']
                tmpFilter["operator"] = request.POST[filter + '_oper']
                if filter == 'size' or filter == 'status':
                    tmpFilter["value2"] = request.POST[filter + '_value2']
                    tmpFilter["operator2"] = request.POST[filter + '_oper2']
                else:
                    tmpFilter["value2"] = ""
                    tmpFilter["operator2"] = ""
                filter_list.append(tmpFilter)
            if 'plot_' + filter in request.POST:
                filter_plot.append(filter)
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
        # Форматирование периода
        period = from_date.strftime('%d/%m/%Y %H:%M') + " - " + to_date.strftime('%d/%m/%Y %H:%M') + " UTC"
        logConst = LogConstruct()
        # Получение параметров GET запроса для выборки
        req = logConst.consructRequest(portal_id, filter_list, from_date, to_date)
        # Получние выборки
        reslog = requests.get(settings.APIURLS['urlLog'] + req, headers=headers)
        if reslog.status_code != 200:
            messages.error(request, "Ошибка выборки логов: " + str(reslog.status_code))
        result = reslog.json()
        if len(filter_plot) == 0:
            data_list = logConst.logPlot(result["data"], ['path', 'user_agent'])
        else:
            data_list = logConst.logPlot(result["data"], filter_plot)
        context = {
            # "value": result,
            "portal": portal,
            "data": data_list,
            "period": period
        }
        return render(request, "log_analyse/results.html", context)

