"""cdn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cdn_projects/', include('cdn_projects.urls')),
    path('stat_cdn/', include('stat_cdn.urls')),
    path('traffic_metric/', include('traffic_metric.urls')),
    path('test_images/', include('test_images.urls')),
    path('log_analyse/', include('log_analyse.urls')),
    path('dnsheader/', include('dnsheader.urls')),
    path('clear_cache/', include('clear_cache.urls')),
    path('', views.index, name='main'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
