"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import mainView, gamesView, contactView,\
    infoView, missingPage,\
    LoginView, LogoutView, CreateUserView,\
    PasswordChangeView, bubbleSwitch, waitingView, PolitykaView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', mainView, name='main'),
    path('waiting/', waitingView, name='my_redirect_field'),
    path('info/', infoView, name='info'),
    path('contact/', contactView.as_view(), name='contact'),
    path('games/', gamesView, name='games'),
    path('maths/', include('maths.urls')),
    path('bubbleSwitch/', bubbleSwitch, name='bubbleSwitch'),
    # path('difference/', missingPage, name='difference' ),
    path('polityka/', PolitykaView, name='polityka' ),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('createuser/', CreateUserView.as_view(), name='createuser'),
    path('changepass/<int:user_id>', PasswordChangeView.as_view(), name='changepass'),

    path('posts/', include('posts.urls')),
    path('moderate/', include('moderate.urls')),

    path('quiz/', include('quiz.urls')),
    path('puzzle/', include('puzzle.urls')),
    path('sudoku/', include('sudoku.urls')),
    path('memo/', include('memo.urls')),
    path('encrypt/', include('encrypt.urls'), name='encrypt'),
    path('difference/', include('difference.urls')),
    path('scoring/', include('scoring.urls')),

    path('maths/fractals/', missingPage, name='encrypt'),
    # path('maths/labirynth/', missingPage, name='encrypt'),
]
