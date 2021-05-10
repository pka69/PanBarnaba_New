from django.urls import path

from .views import moderateView, quizView, quizDetailView, quizAnswerDelete, quizQuestionDelete, libraryListView, libraryMailSend

urlpatterns = [
    path('', moderateView, name='moderate'),
    path('<int:post_type>/', moderateView, name='moderate2'),
    path('<int:post_type>/<action>/<int:id>/', moderateView, name='moderate_action'),
    path('quiz/', quizView, name='moderate_quiz'),
    path('quiz/<int:level>/', quizView, name='moderate_quiz_level'),
    path('quiz_answers/<int:id>/', quizDetailView.as_view(), name="moderate_quiz_answers"),
    path('quiz_answers_item/<int:id>/<int:item_id>/', quizAnswerDelete.as_view(), name="moderate_quiz_answer_delete"),
    path('quiz_delete_item/<int:id>/<int:level>/', quizQuestionDelete.as_view(), name="moderate_quiz_delete"),
    path('library_list/', libraryListView.as_view(), name="library_view"),
    path('library_mail/<template>/<n1>/<n2>/', libraryMailSend, name="library_mail_send"),
    

]

app_name = "moderate"