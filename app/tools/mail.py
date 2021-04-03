from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

from posts.models import Post

AUTHOR = 'autorka'

def moderatorInform():
    moderators = []
    moderate_group = Group.objects.filter(name='moderator').first()
    forum_posts = Post.moderate.filter(group=2).filter(stage=0)
    if forum_posts.count() ==0:
        return False
    for user in moderate_group.user_set.all():
        if user.email: moderators.append(user.email)
    
    if not moderators:
        return False

    context = {
        'posts': forum_posts,
    }

    mail = {
        'subject': 'Są posty do zatwierdzenia',
        'message': render_to_string('mailing/to_moderate.txt', context=context),
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': moderators,
        'html_message': render_to_string('mailing/to_moderate.html', context=context),
        'fail_silently': False
    }
    print('email host', settings.EMAIL_HOST)
    print('email port', settings.EMAIL_PORT)
    print('email user', settings.EMAIL_HOST_USER)
    print('email pass', settings.EMAIL_HOST_PASSWORD)
    print('email default', settings.DEFAULT_FROM_EMAIL)
    print('email SSL', settings.EMAIL_USE_SSL)
    print('email TSL', settings.EMAIL_USE_TLS)
    send_mail(**mail)
    return True
    
def messageToAuthor(id):
    author = User.objects.filter(username=AUTHOR).first()
    if not author:
        return False
    post = Post.notRejected.get(id=id)
    context = {
        'author': author, 
        'title': post.subgroup,
        'content': post.content,
        'mail': post.external_link,
        'picture': post.picture,
    }
    mail = {
        'subject': 'Przyszła wiadomośc do Pana Barnaby/autorki',
        'message': render_to_string('mailing/user_message.txt', context=context),
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [author.email, 'pjkalista@gmail.com'],
        'html_message': render_to_string('mailing/user_message.html', context=context),
        'fail_silently': False
    }
    print('email host', settings.EMAIL_HOST)
    print('email port', settings.EMAIL_PORT)
    print('email user', settings.EMAIL_HOST_USER)
    print('email pass', settings.EMAIL_HOST_PASSWORD)
    print('email default', settings.DEFAULT_FROM_EMAIL)
    print('email SSL', settings.EMAIL_USE_SSL)
    print('email TSL', settings.EMAIL_USE_TLS)
    send_mail(**mail)

def encrypt_to_friend(post, user, path):
    context = {
        'friend': user.username, 
        'path': path,
    }
    mail = {
        'subject': 'Twój znajomy {} rzucił Ci wyzwanie!'.format(user.username),
        'message': render_to_string('mailing/encrypt_challenge_mail.txt', context=context),
        'from_email': settings.DEFAULT_FROM_EMAIL, # user.email if user.email else
        'recipient_list': [post.external_link, 'pjkalista@gmail.com'],
        'html_message': render_to_string('mailing/encrypt_challenge_mail.html', context=context),
        'fail_silently': False
    }
    send_mail(**mail)