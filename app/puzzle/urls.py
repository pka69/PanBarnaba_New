from django.contrib import admin
from django.urls import path
from .views import puzzleView, puzzleSolve

urlpatterns = [
    path('', puzzleView, name='puzzle'),
    path('puzzle_selected/<puzzle_name>', puzzleSolve, name='puzzle_selected'),
]

app_name = "puzzle"