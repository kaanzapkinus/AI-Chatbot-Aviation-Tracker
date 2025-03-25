from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),  # Anasayfa
    path('search/', views.search_flight, name='search_flight'),  # Arama için
]