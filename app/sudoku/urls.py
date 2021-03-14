from django.contrib import admin
from django.urls import path
from .views import sudokuSelectView, sudokuGameView

urlpatterns = [
    path('', sudokuSelectView, name='sudoku'),
    path('<sudoku_type>', sudokuGameView.as_view(), name='sudoku_game'),
    # path('puzzle_selected/<puzzle_name>', sudokuSelected, name='puzzle_selected'),
]
