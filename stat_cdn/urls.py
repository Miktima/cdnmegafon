from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='stat_index'),
    path('results.html', views.results, name='stat_results'),
]