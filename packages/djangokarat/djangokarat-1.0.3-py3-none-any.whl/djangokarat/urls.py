from django.urls import path, include
from django.contrib import admin

from djangokarat.views import SyncData

urlpatterns = [
    path('karat/sync', SyncData.as_view(), name='karat-sync'),
]
