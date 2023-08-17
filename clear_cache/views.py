from django.shortcuts import render
from django.http import JsonResponse
from .forms import ClearCacheForm
from .ClearCache import ClearCache
from django.contrib import messages
from stat_cdnnow.models import Portals_stat

def index(request):
    form = ClearCacheForm()
    return render(request, "clear_cache/index.html", {'form': form})

def results(request):
    if request.method == 'POST':
        form = ClearCacheForm(request.POST)
        if form.is_valid():
            project = request.POST['project']
            if project == 'all':
                portalObj = Portals_stat.objects.order_by('portal').all()
                indexes = ""
                for p in portalObj:
                    indexes += str(p.pk) + ","
                indexes = indexes.rstrip(",")
                masks_field = request.POST['masks']
                context = {
                    "portalObj": portalObj,
                    "indexes": indexes,
                    "masks_field": masks_field
                }
            else:
                portal_ins = Portals_stat.objects.get(pk=project)
                portal = portal_ins.portal
                masks_field = request.POST['masks']
                # формируем лист масок
                masks = []
                if len(masks_field) > 0:
                    masks = masks_field.split(",")
                # Очищаем от пробелов
                for i in range(len(masks)):
                    masks[i] = (masks[i]).strip()
                # При инициализации класса создаются переменные для запроса, включая идентификатор домена в CDN
                # Если идентификатор не найден, возвращаемся на страницу запроса
                if ClearCache(portal) != False:
                    objClearCache = ClearCache(portal)
                else:
                    messages.error(request, ClearCache(portal).error)
                    form = ClearCacheForm()
                    return render(request, "clear_cache/index.html", {'form': form})
                if objClearCache.get_token() != False:
                    token = objClearCache.get_token()
                    # Очищаем кеш по маске
                    if objClearCache.clear_cache(token, masks):
                        if len(masks_field) >0:
                            response = "Cache cleared for: " + masks_field
                        else:
                            response = "All cache cleared"
                    else:
                        messages.error(request, "Cache clear error:" + objClearCache.error)
                        form = ClearCacheForm()
                        return render(request, "clear_cache/index.html", {'form': form})
                else:
                    messages.error(request, "Невозможно получить токен")
                    form = ClearCacheForm()
                    return render(request, "clear_cache/index.html", {'form': form})
                context = {
                    "portal": portal,
                    "response": response
                }
            return render(request, "clear_cache/results.html", context)
        else:
            messages.error(request, "Form is not valid")
            form = ClearCacheForm()
            return render(request, "clear_cache/index.html", {'form': form})
    else:
        form = ClearCacheForm()
        return render(request, "clear_cache/index.html", {'form': form})

def all_clear(request, portal_id):
    if request.method == 'GET':
        portal_ins = Portals_stat.objects.get(pk=portal_id)
        portal = portal_ins.portal
        masks_field = request.COOKIES['masks']
        # формируем лист масок
        masks = []
        if len(masks_field) > 0:
            masks = masks_field.split(",")
        # Очищаем от пробелов
        for i in range(len(masks)):
            masks[i] = (masks[i]).strip()
        # При инициализации класса создаются переменные для запроса, включая идентификатор домена в CDN
        # Если идентификатор не найден, возвращаем false
        if ClearCache(portal) != False:
            objClearCache = ClearCache(portal)
        else:
            status = 'false'
        token = objClearCache.get_token()
        # Очищаем кеш по маске
        if objClearCache.clear_cache(token, masks):
            status = 'true'
        else:
            status = 'false'
        response = {
            "status": status
        }
    return JsonResponse(response)