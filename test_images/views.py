from django.shortcuts import render
from .forms import CdnForm
from django.contrib import messages
import requests
import re
import time

def index(request):
    form = CdnForm()
    return render(request, "test_images/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = CdnForm(request.POST)
        if form.is_valid():
            page_url = request.POST['page_url']
            old_cdn = request.POST['old_cdn']
            # Проверка , что в поле CDN нет слешей
            if old_cdn.find("/") >= 0:
                messages.error(request, 'поле CDN не должно содержать слешей!')
                form = CdnForm()
                return render(request, "test_images/index.html", {'form': form})
            # Если новый CDN не указан, то проверям ссылки со старым CDN 
            if request.POST['new_cdn'] != "":
                new_cdn = request.POST['new_cdn']
                if new_cdn.find("/") >= 0:
                    messages.error(request, 'поле CDN не должно содержать слешей!')
                    form = CdnForm()
                    return render(request, "test_images/index.html", {'form': form})                 
            else:
                new_cdn = old_cdn
            # Загружаем страницу
            response = requests.get(page_url, verify=False)
            # Если страница не загрузилась, то возвращаемся к форме 
            if response.status_code != 200:
                messages.error(request, 'Страница не загружается!')
                form = CdnForm()
                return render(request, "test_images/index.html", {'form': form})
            # Получаем текст страницы
            source = response.text
            # Регулярное выражение для поиска ссылок со старым CDN
            regexp_cdn_domain = old_cdn + "/?([^<?\'\\\" >]+)"
            links_list = []
            # Получаем список всех ссылок со старым CDN
            links_list = re.findall(regexp_cdn_domain, source)
            newcdn_links_list = []
            for l in links_list:
                # Проверяем, что ссылки кончаются буквами и заполняем список с новым CDN
                if re.search("[a-z]$", l) != None:
                    newcdn_links_list.append("https://" + new_cdn + "/" + l)
            # Начальные данные для подсчета статистики
            bad_list = []
            for l in newcdn_links_list:
                # загружаем ссылку
                response_image = requests.get(l, verify=False)
                # Получаем статус
                status = response_image.status_code
                time.sleep(0.3)
                # Если статус не 200, то считаем ошибкой
                if status != 200:
                    bad_list.append([l, status])
            conclusion = "Errors {0:d} from {1:d} urls ({2:.1f}%)".format(len(bad_list), len(newcdn_links_list),\
                (len(bad_list)/len(newcdn_links_list))*100)
            context = {
                "new_cdn": new_cdn,
                "old_cdn": old_cdn,
                "conclusion": conclusion,
                "bad_list": bad_list
            }
            return render(request, 'test_images/results.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CdnForm()
        return render(request, "test_images/index.html", {'form': form})

