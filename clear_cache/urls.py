from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='clearcache_index'),
    path('results.html', views.results, name='clearcache_results')
]