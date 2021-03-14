from django.urls import path

from .views import scoreCheckView, scoreUpdateView

urlpatterns = [
    path('score_check/<game>/<game_id>/<s_result>/<int:hours>/<int:minutes>/<int:seconds>/', scoreCheckView, name='scoreCheck'),
    path('score_update/<game>/<game_id>/<s_result>/<int:hours>/<int:minutes>/<int:seconds>/', scoreUpdateView, name='scoreUpdate'),
    
]