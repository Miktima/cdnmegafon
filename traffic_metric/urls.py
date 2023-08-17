from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='metric_index'),
    path('results.html', views.results, name='metric_results'),
]