from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import requests
from django.conf import settings
import json

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
    context = {
        'portal_list': portal_list,
    }

    return render(request, "clear_cache/index.html", context)

def results(request):
    if request.method == 'POST':
        headers = {'Authorization': 'APIKey ' + settings.APIKEY}
        portal_id = request.POST['portal']
        if portal_id == 'no_select':
            messages.error(request, 'Требуется выбрать портал')
            return HttpResponseRedirect(reverse('log_index'))       
        masks_field = request.POST['masks']
        # Выборка ресурсов
        resources = requests.get(settings.APIURLS['urlResources'] + "/" + portal_id, headers=headers)
        status_code = resources.status_code
        if status_code != 200:
            messages.error(request, "Ошибка выборки портала: " + str(status_code))
            return HttpResponseRedirect(reverse('log_index'))    
        res = resources.json()
        portal = res["cname"]
        if len(res["secondaryHostnames"]) > 0:
            for secCname in res["secondaryHostnames"]:
                portal += "; " + secCname
        # формируем лист масок
        masks = []
        if len(masks_field) > 0:
            masks = masks_field.split(",")
            # Очищаем от пробелов
            for i in range(len(masks)):
                masks[i] = (masks[i]).strip()
        url = (settings.APIURLS['urlClearCache']).replace("{id}", portal_id)
        payload = json.dumps({"paths":masks})
        headers['content-type'] = 'application/json'
        res = requests.post(url, data=payload,  headers=headers)
        status_code = res.status_code
        if status_code == 201:
            result = "Очистка кеша началась"
        else:
            result = "Ошибка!!! Код - " + str(status_code)
        print (res.url)
        print (res.text)
        context = {
            "portal": portal,
            "result": result,
            "mask_field": masks_field
        }
        return render(request, "clear_cache/results.html", context)

