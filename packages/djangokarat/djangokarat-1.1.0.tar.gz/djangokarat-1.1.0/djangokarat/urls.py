from django.urls import path, include
from django.contrib import admin

from djangokarat.views import SyncData, GetKarat

urlpatterns = [
    path('karat/sync', SyncData.as_view(), name='karat-sync'),
    path('karat/ping', GetKarat.as_view(), name='karat-ping'),
]
