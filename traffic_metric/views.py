from django.shortcuts import render
from datetime import date
from stat_cdn.Stat import Statsite
from stat_cdn.MetricPlot import MetricPlot
import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings


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
        'current_day': current_day,
        'metrics': settings.APIMETRICS
    }
    return render(request, "traffic_metric/index.html", context)

def results(request):
    portal_id = request.POST['portal']
    if portal_id == 'no_select':
        messages.error(request, 'Требуется выбрать портал')
        return HttpResponseRedirect(reverse('metric_index'))       
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
    objStat= Statsite()
    # Получение метрик или вывод ошибки в первоначальную форму
    plot_list = []
    for metric in metrics_list:
        # Отправляем запрос на метрику   
        responce = objStat.get_stat(portal_id, from_date, to_date, metric)
        # Если ответ положительный готовим данные для вывода на график
        getPlot = MetricPlot()
        if responce != False:
            data_plot = getPlot.StatPlot(metric, portal_id, responce)
            plot_list.append(data_plot)        
    context = {
        "plot_list": plot_list,
        "portal": portal,
        "from_date": from_date.strftime("%d/%m/%Y"),
        "to_date": to_date.strftime("%d/%m/%Y")
    }
    return render(request, 'traffic_metric/results.html', context)
