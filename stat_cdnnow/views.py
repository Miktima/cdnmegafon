from django.shortcuts import render
from .models import Portals_stat
from datetime import date
from .Stat import Statsite
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from io import BytesIO
import base64

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def index(request):
    # Выбираем список порталов
    portal_list = Portals_stat.objects.order_by("portal").all()
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
    return render(request, "stat_cdnnow/index.html", context)

def results(request):
    portal_id = request.POST['portal']
    try:
        portal_obj = Portals_stat.objects.get(id_portal=portal_id)
    except Portals_stat.DoesNotExist:
        # Если портал не выбран или не найден, повторяем вывод формы
        messages.error(request, 'Необходимо выбрать портал')
        return HttpResponseRedirect(reverse('stat_index'))
    else:
        objStat = Statsite()
        # Статистика собирается за указанный день, или за месяц, если день не указан
        year_stat = int(request.POST['year'])
        month_stat = int(request.POST['month'])
        if request.POST['day'] == "no":
            day_stat = ""
        else:
            day_stat = int(request.POST['day'])
        stat_period = [year_stat, month_stat, day_stat]
        if objStat.get_token() != False:
            token = objStat.get_token()
            # Если токен получен, отправляем запрос
            response = objStat.get_stat(token, request.POST['portal'], stat_period)
            # Если ответ положительный готовим данные для вывода на график
            if response != False:
                plot_y = []
                plot_x = []
                for key, value in response.items():
                    f = (list(value.values()))[0]
                    plot_y.append(f)
                    plot_x.append(key)
                plt.plot(plot_x, plot_y)
                plt.ylabel('TB')
                if day_stat == "":
                    plt.xlabel('Days')
                else:
                    plt.xlabel('Hours')
                plt.autoscale()
                # График сохраняем в памяти и передаем в шаблон
                img_in_memory = BytesIO()
                plt.savefig(img_in_memory, format="png")
                data_plot = base64.b64encode(img_in_memory.getvalue()).decode()
                plt.clf()
        # Форматирование вывода периода для шаблона
        if day_stat == "":
            period = str(month_stat) + "/" + str(year_stat)
        else:
            period = str(day_stat) + "/" + str(month_stat) + "/" + str(year_stat)
        context = {
            "portal": portal_obj.portal,
            "plot": data_plot,
            "period": period
        }
        return render(request, 'stat_cdnnow/results.html', context)