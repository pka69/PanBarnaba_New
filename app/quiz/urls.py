from django.urls import path

from .views import quizListView, quizPlayView, quizNextView

urlpatterns = [
    path('', quizListView.as_view(), name='quiz_list'),
    path('<int:qlevel>/<qgroup>', quizPlayView.as_view(), name='quiz_play'),
    path('next/<int:qlevel>/<qgroup>', quizNextView.as_view(), name='quiz_next_play'),
]