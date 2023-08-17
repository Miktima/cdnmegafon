from django.shortcuts import render

def index(request):
    applications = {
        "stat_cdnnow/": "Получение статистики трафика через API",
        "traffic_metric/": "Получение метрик трафика через API",
        "test_images/": "Проверка загрузки изображений через CDN",
        "test_cash/": "Проверка кеширования контента в CDN",
        "log_analize/": "Анализ лог файла CDN",
        "dnsheader/": "Сведения о DNS домена и HTTP заголовках",
        "clear_cache/": "Очистка кеша в CDN" 
    }
    context = {
        "applications": applications
    }
    return render(request, "cdn/index.html", context=context)