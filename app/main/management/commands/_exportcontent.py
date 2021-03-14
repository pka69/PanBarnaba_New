from os.path import join
import json

from django.conf import settings

from posts.models import Post
from quiz.models import Question, Answer

SEL_POST_TYPE = (
    # (0, 'News'),  # newses from internet
    # (1, 'Quotation'),  # quotation from books
    # (3, 'Notes'),  # notes from author
    # (4, 'Post'),  # special post for website
    # (6, 'Content'),  # website content
    (8, 'Welcome'),
)
SEL_POST_TYPE_ID = [item[0] for item in SEL_POST_TYPE]

mypath = settings.STATICFILES_DIRS[0] / 'others'


def changeHTML():
    posts = Post.objects.filter(group__in=SEL_POST_TYPE_ID)
    for post in posts:
        post.content = post.content.replace('<br>', '')
        post.save()


def exportContent():
    posts = Post.objects.filter(group__in=SEL_POST_TYPE_ID)
    with open(join(mypath, 'content.json'), "w") as f:
        json.dump([post.export() for post in posts], f)
    return posts.count()


def importContent():
    with open(join(mypath, 'content.json'), "r") as f:
        data = json.load(f)
    for item in data:
        Post.objects.create(**item)
    return len(data)