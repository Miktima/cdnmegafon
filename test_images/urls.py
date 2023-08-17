from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='img_index'),
    path('results.html', views.results, name='img_results'),
]