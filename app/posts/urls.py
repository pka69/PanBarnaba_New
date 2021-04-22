from django.urls import path
from .views import bookstorePricesView, newsView, forumView, forumReactView, forumRulesView

urlpatterns = [
    path('bookpricelist/', bookstorePricesView, name='bookpricelist'),
    # path('bookpricelist/<subgroup>/', bookstorePricesView, name='bookpricelist_subgroup'),
    path('news/', newsView, name='news'),
    path('rules/', forumRulesView, name="forum_rules"),
    path('forum/', forumView.as_view(), name='forum'),
    path('forum/<int:ftype>/', forumView.as_view(), name='forum_selected'),
    path('forum-react/<react>/<int:post_id>/', forumReactView.as_view()),
    path('forum-react/<react>/<ftype>/<int:post_id>/', forumReactView.as_view()),
]
