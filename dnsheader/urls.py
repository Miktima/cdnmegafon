from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dns_index'),
    path('results.html', views.results, name='dns_results'),
]