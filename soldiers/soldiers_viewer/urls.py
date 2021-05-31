
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('about', views.about, name='about'),
    path('map', views.map, name='map'),
    path('map/data', views.map_data, name='map_data')
]
