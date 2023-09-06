from django.shortcuts import render
from django.conf import settings
import json
import requests

def index(request):
    headers = {'Authorization': 'APIKey ' + settings.APIKEY}
    # Выборка ресурсов
    resources = requests.get(settings.APIURLS['urlResources'], headers=headers)
    status_code = resources.status_code
    res = resources.json()
    # Выборка источников
    sources = requests.get(settings.APIURLS['urlSourceGroups'], headers=headers)
    sour = sources.json()
    result = []
    # заполняем результат для показа
    for r in res:
        resDict = {}
        resDict["id"] = r["id"]
        resDict["descrition"] = r["description"]
        resDict["cname"] = r["cname"]
        # Выбираем по номеру группы источников сами источники, чтобы потом вставить в таблицу
        for s in sour:
            if r["originGroup"] == s["id"]:
                sourStr = ""
                # Если источников несколько, записываем через точку с запятой
                for ss in s["origins"]:
                    if len(sourStr) > 0:
                        sourStr += "; "
                    sourStr += ss["source"]
                resDict["origin"] = sourStr
                break
        result.append(resDict)
    context = {
        "status_code": status_code,
        "response": result
    }
    return render(request, "cdn_projects/index.html", context)