from random import choice
import json

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


from main.models import Menu
from main.views import getBubbles, getBubblesLike
from posts.models import Post
from tools.mail import encrypt_to_friend
from .encrypt import Sylabowy, Brownie, Divider, Kaczor, isCorrect, getEncryptor

# Create your views here.
context = {}

GADERYPOLUKI = Sylabowy.GADERYPOLUKI
KACZOR = Kaczor.KACZOR


def gaderypolukiView(request, level=0):
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "szyfr GADERYPOLUKI"
    context['method'] = "gaderypoluki"
    context['logo'] = 'gaderypoluki.png'
    if level:
        context['key'] = choice(GADERYPOLUKI)
        quotation = choice([item for item in Post.notRejected.filter(group=1).filter(subgroup='encrypt-{}'.format(level))])
        context['quotation'] = quotation.id
        hash = Sylabowy(quotation.content, context['key'])
        context['encrypt'] = hash.getEncrypted()
        context['key_view'] = hash.getKey()
        context['level'] = level
        context['rows'] = level * 100
        return render(request, 'encrypt/gaderypoluki_selected.html', context=context)
    return render(request, 'encrypt/gaderypoluki.html', context=context)


def brownieView(request, level=0):
    # show all defined encryptors
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "szyfr Czekoladka"
    context['method'] = "brownie"
    context['logo'] = 'czekoladka.png'
    if level:
        
        quotation = choice([item for item in Post.notRejected.filter(group=1).filter(subgroup='encrypt-{}'.format(level))])
        context['quotation'] = quotation.id
        hash = Brownie(quotation.content)
        context['key'] = hash.key
        context['encrypt'] = hash.getEncrypted()
        context['level'] = level
        context['rows'] = level * 100
        return render(request, 'encrypt/brownie_selected.html', context=context)
    return render(request, 'encrypt/brownie.html', context=context)
    

def dividerView(request, level=0):
    # show all defined encryptors
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "szyfr ułamkowy"
    context['method'] = "divider"
    context['logo'] = 'divider.png'
    if level:
        
        quotation = choice([item for item in Post.notRejected.filter(group=1).filter(subgroup='encrypt-{}'.format(level))])
        context['quotation'] = quotation.id
        hash = Divider(quotation.content)
        context['key'] = hash.key
        context['encrypt'] = hash.getEncrypted()
        context['level'] = level
        context['rows'] = level * 100
        return render(request, 'encrypt/divider_selected.html', context=context)
    return render(request, 'encrypt/divider.html', context=context)


def kaczorView(request, level=0):
    # show all defined encryptors
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "szyfr Kaczor"
    context['KACZOR'] = KACZOR
    context['method'] = "kaczor"
    context['logo'] = 'kaczor.png'
    if level:
        quotation = choice([item for item in Post.notRejected.filter(group=1).filter(subgroup='encrypt-{}'.format(level))])
        context['quotation'] = quotation.id
        hash = Kaczor(quotation.content)
        context['key'] = hash.key
        context['encrypt'] = hash.getEncrypted()
        context['level'] = level
        context['rows'] = level * 100
        return render(request, 'encrypt/kaczor_selected.html', context=context)
    return render(request, 'encrypt/kaczor.html', context=context)

@csrf_exempt
def checkEncrypt(request):  #  , method, encrypt_key, to_check
    # return success or error user encryption
    if request.method=="POST":
        body = json.loads(request.body.decode())
        quotation = Post.notRejected.get(pk=int(body['id']))
        try:
            friend_message = json.loads(quotation.content)
        except ValueError:
            result = isCorrect(body['method'], body['key'], quotation.content, body['answer'])
        else:
            result = isCorrect(body['method'], body['key'], friend_message['to_encrypt'], body['answer'])
    response = {
        "status": "success" if result else "error",
        "quotation": quotation.content,
        "method": body['method'],
        "encrypt_key": body['key'],
        "user_answer": body['answer'],
    }
    return JsonResponse(response)


@login_required
def encryptMessageView(request):
    if request.method=="POST":
        user_id = int(request.user.id)
        method = request.POST.get('method_id','')
        key = request.POST.get('key_id','')
        email = request.POST.get('email','')
        to_encrypt = request.POST.get('to_encrypt','')
        user = User.objects.get(pk=user_id)
        path = request.get_host()
        body = {
            'method': method, 
            'key': key,
            'to_encrypt': to_encrypt
        }
        json_body = json.dumps(body)
        try:
            post = Post.notRejected.create(
                group=9,
                subgroup="encrypt",
                content = json_body,
                external_link = email,
                stage = 0,
                dec_content = 0
            )
        except Exception:
            messages.error('Wystąpił niespodziewany błąd')
        else:
            path = path +'/encrypt/challenge/{}/'.format(post.id)
            encrypt_to_friend(post, user, path)
            messages.info(request, 'Wiadomość została wysłana'.format(path))
        redirect('/')
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "Zaproś znajomych do zabawy!"
    context['methods'] = ENCRYPT_ACTION.keys
    context['sylabowy'] = GADERYPOLUKI
    return render(request, 'encrypt/encrypt_friend_message.html', context=context)

def challengeView(request, id):
    post = Post.notRejected.get(pk=id)
    body = json.loads(post.content)
    post.dec_content +=1
    post.save()
    hash = getEncryptor(body['method'], body['key'], body['to_encrypt'])
    context = {
        'method': body['method'], 
        'key': body['key'],
        'friend': post.owner,
    }
    context['key_view'] = hash.getKey()
    context['encrypt'] = hash.getEncrypted()
    context['level'] = 3
    context['rows'] = 100
    context['quotation'] = post.id
    context['submenu'] = Menu.getMenu('main')
    context['PB_Stories'] = getBubblesLike(request)
    context['title'] = "Odkoduj zaszyfrowaną wiadomość!"
    return render(request, 'encrypt/encrypt_challenge.html', context=context)


# ENCRYPT_ACTION list name of encrypt method related with views
ENCRYPT_ACTION = {
    'brownie': brownieView, 
    'gaderypoluki': gaderypolukiView,
    'divider': dividerView, 
    'kaczor': kaczorView,
    'challenge': challengeView,
}

def encryptView(request, action='', level=0, level2=0 ):
    # show all defined encryptors
    if action:
        if level2:
            return ENCRYPT_ACTION[action](request, level2)
            
        if level:
            return ENCRYPT_ACTION[action](request,level)
            
        return ENCRYPT_ACTION[action](request)
        
    context['submenu'] = Menu.getMenu('main')
    context['games'] = Menu.getMenu('encrypt', detail=1)
    context['PB_Stories'] = getBubbles(request)
    context['title'] = "Pobaw się w szyfrowanie"
    context['logo'] = 'encrypt.png'
    return render(request, 'encrypt/encrypt.html', context=context)