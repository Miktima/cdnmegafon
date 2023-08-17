from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cash_index'),
    path('results.html', views.results, name='cash_results'),
]