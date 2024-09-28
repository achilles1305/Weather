from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bycity/', views.index, name='by_city'),
    path('bymap/', views.map_view, name='by_map'),
    path('get_weather/', views.get_weather, name='get_weather'),
]
