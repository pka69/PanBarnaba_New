from django.contrib import admin
from django.urls import path
from .views import differenceView, differenceSolve

urlpatterns = [
    path('', differenceView, name='difference'),
    path('difference_selected/<picture_name>', differenceSolve, name='difference_selected'),
]
