from django.shortcuts import render

def index(request):
    applications = {
        "cdn_projects/": "Список проектов CDN",
        "stat_cdn/": "Получение статистики трафика через API",
        "traffic_metric/": "Получение метрик трафика через API",
        "test_images/": "Проверка загрузки изображений через CDN",
        "log_analyse/": "Анализ логов CDN",
        "dnsheader/": "Сведения о DNS домена и HTTP заголовках",
        "clear_cache/": "Очистка кеша в CDN" 
    }
    context = {
        "applications": applications
    }
    return render(request, "cdn/index.html", context=context)