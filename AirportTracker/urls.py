from django.urls import path
from . import views

app_name = 'airporttracker'  # optional: for namespacing your URLs

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_flight, name='search_flight'),
    path('chat/', views.chat_assistant, name='chat_assistant'),
]