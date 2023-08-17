import requests
import time

with open("key.txt") as f:
    APIkey = f.read().strip()
urlService = "https://api.lk.cdn.megafon.ru/cdn/clients/me"
urlServiceFeatures = "https://api.lk.cdn.megafon.ru/cdn/clients/me/features"
urlSourceGroups = "https://api.lk.cdn.megafon.ru/cdn/source_groups"
headers = {'Authorization': 'APIKey ' + APIkey}
r = requests.get(urlSourceGroups, headers=headers)
print ("Status code: ", r.status_code)
print ("Content: ", r.json())