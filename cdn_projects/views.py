from django.shortcuts import render
import json
import requests

def index(request):
    with open("../key.txt") as f:
        APIkey = f.read().strip()
    with open('../urls.json') as json_file:
        urls = json.load(json_file)
    headers = {'Authorization': 'APIKey ' + APIkey}
    resources = requests.get(urls['urlResources'], headers=headers)
    return render(request, "clear_cache/results.html", context)