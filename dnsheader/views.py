import dns.resolver
import re
import requests
from django.shortcuts import render
from .forms import DnsForm



def index(request):
    form = DnsForm()
    return render(request, "dnsheader/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = DnsForm(request.POST)
        if form.is_valid():
            domain = form.cleaned_data["domain"]
            cdn = form.cleaned_data["cdn"]
            # Результаты сохраняем в лист
            result_domain = []
            result_http = []
            # Получаем результаты для домена с img. и без .img
            try:
                response = requests.get("https://" + domain, verify=False)            
                result_http.append({
                    "query": True,
                    "url": "https://" + domain,
                    "status_code": response.status_code,
                    "history": response.history,
                    "headers": response.headers
                })
            except requests.ConnectionError:
                result_http.append({
                    "query": False,
                    "url": "https://" + domain,
                    "error": "A Connection error occurred",
                })
            try:
                result_domain.append({
                    "query": True,
                    "result": dns.resolver.resolve(domain, 'A')
                })
            except  dns.resolver.NXDOMAIN:
                result_domain.append({
                    "query": False,
                    "qname": domain,
                    "error": "NXDOMAIN: The DNS query name does not exist"
                })
            # И для второго домена
            if re.search("^img.*", domain):
                domain = domain.replace("img.", "")
            else:
                domain = "img." + domain
            try:
                response = requests.get("https://" + domain, verify=False)            
                result_http.append({
                    "query": True,
                    "url": "https://" + domain,
                    "status_code": response.status_code,
                    "history": response.history,
                    "headers": response.headers
                })
            except requests.ConnectionError:
                result_http.append({
                    "query": False,
                    "url": "https://" + domain,
                    "error": "A Connection error occurred",
                })
            try:
                result_domain.append({
                    "query": True,
                    "result": dns.resolver.resolve(domain, 'A')
                })
            except  dns.resolver.NXDOMAIN:
                result_domain.append({
                    "query": False,
                    "qname": domain,
                    "error": "NXDOMAIN: The DNS query name does not exist"
                })                
            # Если в списке cdn нет запятой, то указан один адрес. Если есть, то несколько
            result_cdn = []
            result_http_cdn = []
            if cdn.find(",") >0:
                cdn_list = cdn.split(",")
                for c in cdn_list:
                    try:
                        result_cdn.append({
                            "query": True,
                            "result": dns.resolver.resolve(c.strip(), 'A')
                        })
                    except  dns.resolver.NXDOMAIN:
                        result_cdn.append({
                            "query": False,
                            "qname": c.strip(),
                            "error": "NXDOMAIN: The DNS query name does not exist"
                        })                
                    try:
                        response = requests.get("https://" + c.strip(), verify=False)            
                        result_http_cdn.append({
                            "query": True,
                            "url": "https://" + c.strip(),
                            "status_code": response.status_code,
                            "history": response.history,
                            "headers": response.headers
                        })
                    except requests.ConnectionError:
                        result_http_cdn.append({
                            "query": False,
                            "url": "https://" + c,
                            "error": "A Connection error occurred",
                        })
            else:
                try:
                    response = requests.get("https://" + cdn, verify=False)            
                    result_http_cdn.append({
                        "query": True,
                        "url": "https://" + cdn,
                        "status_code": response.status_code,
                        "history": response.history,
                        "headers": response.headers
                    })
                except requests.ConnectionError:
                    result_http_cdn.append({
                        "query": False,
                        "url": "https://" + cdn,
                        "error": "A Connection error occurred",
                    })
                try:
                    result_cdn.append({
                        "query": True,
                        "result": dns.resolver.resolve(cdn, 'A')
                        })
                except  dns.resolver.NXDOMAIN:
                    result_cdn.append({
                        "query": False,
                        "qname": cdn,
                        "error": "NXDOMAIN: The DNS query name does not exist"
                    })
                     
            context = {
                "domain": domain,
                "result_domain": result_domain,
                "result_cdn": result_cdn,
                "result_http": result_http,
                "result_http_cdn": result_http_cdn,
            }
            return render(request, 'dnsheader/results.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DnsForm()
        return render(request, "dnsheader/index.html", {'form': form})
