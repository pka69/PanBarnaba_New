from django.contrib import admin
from django.urls import path
from .views import memoView, memoSolveView

urlpatterns = [
    path('', memoView, name='memo'),
    path('memo_selected/<int:level>', memoSolveView, name='memo_selected'),
]
app_name = "memo"