from django.shortcuts import render
from .forms import CashForm
from .Test_Cash import TestCashSite
from django.contrib import messages
import requests
import re
import time
import random

def index(request):
    form = CashForm()
    return render(request, "test_cash/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = CashForm(request.POST)
        if form.is_valid():
            page_url = request.POST['page_url']
            cdn = request.POST['cdn']
            # Проверка , что в поле CDN нет слешей
            if cdn.find("/") >= 0:
                messages.error(request, 'поле CDN не должно содержать слешей!')
                form = CashForm()
                return render(request, "test_cash/index.html", {'form': form})
            # Загружаем тестируемую страницу и проверяем, что она загрузилась
            response = requests.get(page_url, verify=False)
            if response.status_code != 200:
                messages.error(request, 'Страница не может быть загружена!')
                form = CashForm()
                return render(request, "test_cash/index.html", {'form': form})
            # Получаем текст страницы
            source = response.text
            # Получаем домен страницы
            domain = (re.search("^https://([A-Za-z_0-9.-]+).*", page_url)).group(1)
            # Формируем регулярный запрос для подготовки ссылок
            regexp_cdn_domain = cdn + "/?([^<?\'\\\" >]+)"
            # Список всех ссылок
            links_list = []
            # Список тестируемых ссылок
            links = []
            links_list = re.findall(regexp_cdn_domain, source)
            lenlist = len(links_list)
            # Если ссылок не найдено, переходим к форме
            if lenlist == 0:
                messages.error(request, 'ERROR: CDN content was not be found on the page!')
                form = CashForm()
                return render(request, "test_cash/index.html", {'form': form})
            # Если ссылок меньше или равно 10 копируем все и удаляем те, которые заканчиваются на слеш
            elif lenlist > 0 and lenlist <= 10:
                for i in lenlist:
                    if links_list[i].endswith("/") == True:
                        links.append(links_list[i])
            # Если ссылок больше 10, выбираем случайно
            elif lenlist > 10:
                random.seed()
                i = 0
                # Чтобы ссылки не повторялись, запоминаем выбранные номера в новом списке
                choose_list = []
                # Должно быть 10 ссылок
                while i < 10:
                    # Определяем переменную для цикла
                    new_n = True
                    # Делаем цикл пока не нашли новый номер 
                    while new_n:
                        n = random.randrange(0, lenlist)
                        # Если такой номер раньше не выбирался и ссылка не заканчивается на слеш
                        if choose_list.count(n) == 0 and (links_list[n]).endswith("/") == False:
                            # Добавляем в спиок новый номер
                            choose_list.append(n)
                            # добавляем единицу и выходим из цикла поиска новой ссылки
                            i += 1
                            new_n = False
                # Заполняем ссылки для тестирования, используя список выбранных номеров
                for k in range(0, 10):
                    links.append(links_list[choose_list[k]])
            # При инициализации класса создаются переменные для запроса, включая идентификатор домена в CDN
            # Если идентификатор не найден, возвращаемся на страницу запроса
            if TestCashSite(domain) != False:
                objTest = TestCashSite(domain)
            else:
                messages.error(request, TestCashSite(domain).error)
                form = CashForm()
                return render(request, "test_cash/index.html", {'form': form})
            if objTest.get_token() != False:
                token = objTest.get_token()
                # В течение 10 секунд пытаемся получить нужный статус, если не получается, то выходим
                i = 0
                for i in range(10):
                    if objTest.get_status(token) != False:
                        break 
                    time.sleep(1)
                    i += 1
                    if i == 9:
                        # Если невозможно получить положительный статус, рекомендуется проверить статус на сайте CDNNOW
                        messages.error(request, "Невозможно получить положительный статус. Проверьте статус на CDNNOW")
                        form = CashForm()
                        return render(request, "test_cash/index.html", {'form': form})
                # Проверяем статус запроса каждые 5 секунд
                if objTest.test_link(token, links):
                    time.sleep(5)
                    while objTest.check_test_status(token) != "passed":
                        time.sleep(5)
                    # Получаем результат
                    results = objTest.get_test_result(token)
                    results_list = []
                    for key, values in results.items():
                        for i in values:
                            results_list.append(["https://" + cdn + "/" + key, i])
                    objTest.terminate_test(token)
                else:
                    messages.error(request, objTest.error)
                    form = CashForm()
                    return render(request, "test_cash/index.html", {'form': form})
            else:
                messages.error(request, "Невозможно получить токен")
                form = CashForm()
                return render(request, "test_cash/index.html", {'form': form})
        context = {
            "portal": domain,
            "results": results_list,
        }
        return render(request, "test_cash/results.html", context)
    else:
        form = CashForm()
        return render(request, "test_cash/index.html", {'form': form})
