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
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap, EncryptSitemap

from main.views import mainView, gamesView, contactView,\
    infoView, missingPage,\
    LoginView, LogoutView, CreateUserView,\
    PasswordChangeView, bubbleSwitch, waitingView, PolitykaView

sitemaps = {
   'static': StaticSitemap,
   'encrypt_method': EncryptSitemap,
}



urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls, name='admin'),

    path('', mainView, name='main'),
    path('waiting/', waitingView, name='my_redirect_field'),
    path('info/', infoView, name='info'),
    path('contact/', contactView.as_view(), name='contact'),
    path('games/', gamesView, name='games'),
    path('bubbleSwitch/', bubbleSwitch, name='bubbleSwitch'),
    # path('difference/', missingPage, name='difference' ),
    path('polityka/', PolitykaView, name='polityka' ),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('createuser/', CreateUserView.as_view(), name='createuser'),
    path('changepass/<int:user_id>', PasswordChangeView.as_view(), name='changepass'),

    path('posts/', include('posts.urls', namespace='posts'), name="posts"),
    path('moderate/', include('moderate.urls', namespace='moderate')),
    path('maths/', include('maths.urls', namespace='maths')),

    path('quiz/', include('quiz.urls', namespace='quiz')),
    path('puzzle/', include('puzzle.urls', namespace='puzzle')),
    path('sudoku/', include('sudoku.urls', namespace='sudoku')),
    path('memo/', include('memo.urls', namespace='memo')),
    path('encrypt/', include('encrypt.urls', namespace='encrypt'), name='encrypt'),
    path('difference/', include('difference.urls', namespace='differences')),
    path('scoring/', include('scoring.urls', namespace='scoring')),

    path('maths/fractals/', missingPage, name='fractals'),
    # path('maths/labirynth/', missingPage, name='encrypt'),
]
