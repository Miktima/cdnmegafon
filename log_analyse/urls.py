from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='log_index'),
    path('results.html', views.results, name='log_results'),
]