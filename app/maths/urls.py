from django.urls import path

from .views import gameOfLifeView, gameOfLifeGoView, labirynthView, labirynthGoView
from main.views import mathsView

urlpatterns = [
    path('', mathsView, name='maths'),
    path('life/', gameOfLifeView.as_view(), name='game_of_life'),
    path('life-go/', gameOfLifeGoView.as_view(), name='game_of_life_go'),
    path('labirynth/', labirynthView.as_view(), name='labirynth'),
    path('labirynth-go/', labirynthGoView.as_view(), name='labirynth_go'),

]   