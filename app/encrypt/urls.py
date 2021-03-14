from django.urls import path

from .views import encryptView, checkEncrypt, encryptMessageView, challengeView
from main.views import missingPage

urlpatterns = [
    path('', encryptView, name='mainEncrypt'),
    path('check_answer_is_correct/', checkEncrypt, name='checkEncrypt'),
    path('challenge/<int:id>', challengeView, name='encryptChallengeView'),
    path('message_to_friend/', encryptMessageView, name="friendMessageView"),
    path('<action>/', encryptView, name='specificEncrypt'),
    path('<action>/<int:level>/', encryptView, name='selectedEncrypt'),
    path('<action>/<int:level>/<int:level2>/', encryptView, name='selectedEncrypt'),
   

    # path('gaderypoluki/', gaderypolukiView, name='gaderypoluki'),
    # path('gaderypoluki/<int:level>/', gaderypolukiView, name='gaderypoluki_selected'),
    # path('brownie/', brownieView, name='brownie'),
    # path('brownie/<int:level>/', brownieView, name='brownie_selected'),
    # path('divider/', dividerView, name='divider'),
    # path('divider/<int:level>/', dividerView, name='divider_selected'),
    # path('kaczor/', kaczorView, name='kaczor'),
    # path('kaczor/<int:level>/', kaczorView, name='kaczor_selected'),
]