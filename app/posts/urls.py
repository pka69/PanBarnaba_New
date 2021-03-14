from django.urls import path
from .views import bookstorePricesView, newsView, forumView, forumReactView

urlpatterns = [
    path('bookpricelist/', bookstorePricesView, name='bookpricelist'),
    path('bookpricelist/<subgroup>/', bookstorePricesView, name='bookpricelist_subgroup'),
    path('news/', newsView, name='news'),
    path('forum/', forumView.as_view(), name='forum'),
    path('forum/<ftype>/', forumView.as_view(), name='forum_selected'),
    path('forum-react/<react>/<int:post_id>/', forumReactView.as_view()),
    path('forum-react/<react>/<ftype>/<int:post_id>/', forumReactView.as_view()),
]
