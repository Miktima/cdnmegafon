from django.shortcuts import render
from django.conf import settings
import json
import requests

def index(request):
    headers = {'Authorization': 'APIKey ' + settings.APIKEY}
    resources = requests.get(settings.APIURLS['urlResources'], headers=headers)
    status_code = resources.status_code
    res = resources.json()
    sources = requests.get(settings.APIURLS['urlSourceGroups'], headers=headers)
    sour = sources.json()
    context = {
        "status_code": status_code,
        "response": res,
        "sources": sour
    }
    return render(request, "cdn_projects/index.html", context)