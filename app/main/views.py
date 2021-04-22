'''
main application module. 
collecting standard functionality: logi/logout/create user/change password
additionally contact view, info view, gamesview and maths view
'''
from datetime import datetime
import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin # to delete in final project
from django.views.generic.edit import CreateView, FormView
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.decorators import login_required  # to delete in final project


from .forms import LoginForm, CreateUserForm, PasswordChangeForm
from .models import Menu
from posts.models import Post
from puzzle.puzzle import puzzleList
from moderate.views import paginate
from tools.mail import messageToAuthor

PAGE_RECORDS = 5

premier_time = datetime(2021, 4, 14, 10, 0, 0)  # book premiere date

context = {
    'premier_time': [
        premier_time.year,
        premier_time.month,
        premier_time.day,
        premier_time.hour,
        premier_time.minute,
        premier_time.second,
    ] if premier_time > datetime.now() else None,
}


def missingPage(request):
    # info view, that final view is under construction
    context['submenu'] = Menu.getMenu('main')
    return render(request, 'page_under_construction.html', context=context)

def getBubbles(request):
    if request.session.get('bubbles', 'yes') == 'no':
        return []
    return Post.notRejected.filter(group=6).filter(subgroup=request.path).order_by('subgroup')

def getBubblesLike(request):
    if request.session.get('bubbles','yes') == 'no':
        return []
    return Post.notRejected.filter(group=6).filter(subgroup__startswith=request.path).order_by('subgroup')


def waitingView(request):
    pass


def mainView(request):
    '''
    main view.
    in menu link to the all functionality,
    main block shows games and maths,
    right block shows all last info like last forum post, lats nes, actual best price in bookstores
    in bottom bar info about current user, button to login/logout/create user/change password
    '''

    # if request.session.get('intro', 'brak') == 'brak':
    #     request.session['intro'] = 'OK'
    #     return redirect('/intro/')
    if not request.session.get('welcome'):
        messages.info(request, 'Witaj! {}'.format(Post.welcome()))
        request.session['welcome'] = True
    context['submenu'] = Menu.getMenu('main')
    context['games'] = Menu.getMenu('games', detail=1)
    context['maths'] = Menu.getMenu('maths', detail=1)
    context['puzzle'] = puzzleList('images/carousel')
    context['content'] = Post.notRejected.filter(group=6).filter(subgroup__startswith="main-carusel").order_by('subgroup')
    context['sections'] = Post.notRejected.filter(group=6).filter(subgroup__startswith="main-section").order_by('subgroup')
    context['news'] = Post.notRejected.filter(group=0)[:4]
    context['forum'] = Post.approved.filter(group=2).filter(related_post__isnull=True)[:4]
    # context['bookstore'] = Post.bookBestPrice('książka')
    # context['ebookstore'] = Post.bookBestPrice('ebook')
    context['PB_Stories'] = getBubbles(request)
    return render(request, 'NL_main.html', context=context)


def introView(request):
    if not request.session.get('welcome'):
        messages.info(request, 'Witaj! {}'.format(Post.welcome()))
        request.session['welcome'] = True
    context['submenu'] = Menu.getMenu('main')
    context['puzzle'] = puzzleList('images/carousel')
    context['content'] = Post.notRejected.filter(group=6).filter(subgroup__startswith="main-carusel").order_by('subgroup')
    page = int(request.GET.get('page', 1))
    context['posts'] = paginate(Post.notRejected.filter(group=0), page)
    context['games'] = Menu.getMenu('games', detail=1)
    context['maths'] = Menu.getMenu('maths', detail=1)
    return render(request, 'intro.html', context=context)


def infoView(request):
    # show info view
    context['submenu'] = Menu.getMenu('main')
    context['title'] = 'Garść informacji ogólnych'
    context['logo'] = 'info.png'
    context['PB_Stories'] = getBubbles(request)
    return render(request, 'info.html', context)


class contactView(View):
    
    def get(self, request):
        # show contact view with possibility so send message to the author
        context['submenu'] = Menu.getMenu('main')
        context['logo'] = 'kontakt.png'
        context['title'] = ' '  #skontaktuj się z nami
        context['PB_Stories'] = getBubbles(request)
        return render(request, 'contact.html', context=context)
    
    def post(self, request):
        user_id = request.POST.get('user', 0)
        group = request.POST.get("group", 7)
        subgroup = request.POST.get("subgroup", 0)
        content = request.POST.get("content", 0)
        picture = request.FILES.get('pictureFile', None)
        external_link = request.POST.get('external_link', '')

        # try:
        #     user = User.objects.get(pk=user_id)
        # except Exception as e:
        #     messages.error(request, 'Wystąpił błąd. Aby zostawić wiadomość trzeba być zalogowanym')
        #     return redirect('/')
        if user_id:
            user = User.objects.get(pk=user_id)
            msg = Post.notRejected.create(group=group,
                subgroup=subgroup,
                content=content,
                owner=user,
                external_link=external_link,
            )
        else:
            msg = Post.notRejected.create(group=group,
                subgroup=subgroup,
                content=content,
                external_link=external_link,
            )
        if picture:
            mypath = settings.DEPLOY_ROOT / 'images/messages'
            filename = picture.name
            full_name = os.path.join(mypath, filename)
            open(full_name, 'wb').write(picture.file.read()) 
            msg.picture = '/images/messages/' + filename
            msg.save()
        messages.success(request, 'Dziękujemy za zostawioną wiadomość')
        messageToAuthor(msg.id)
        return redirect('/')


def gamesView(request):
    # show all defined games
    context['submenu'] = Menu.getMenu('main')
    context['games'] = Menu.getMenu('games', detail=1)
    context['PB_Stories'] = getBubbles(request)
    context['title'] = 'Wybierz grę dla siebie'
    context['logo'] = 'play.png'
    return render(request, 'games.html', context=context)


def mathsView(request):
    # show all defined maths info
    context['submenu'] = Menu.getMenu('main')
    context['maths'] = Menu.getMenu('maths', detail=1)
    context['PB_Stories'] = getBubbles(request)
    context['title'] = 'Zobacz co przygotowaliśmy'
    context['logo'] = 'play.png'
    return render(request, 'maths.html', context=context)


def bubbleSwitch(request):
    if request.session.get('bubbles','yes') == 'no':
        request.session['bubbles'] = 'yes'
    else:
        request.session['bubbles'] = 'no'
    next = request.GET.get('next', '/')
    return redirect(next)


class LoginView(View):
    # acces to loginform
    def get(self, request):
        if request.user.id:
            messages.warning(request, 'Prawdopodobnie nie masz odpowiednich uprawnień do wejścia na tę strone')
            return redirect('/')
        form = LoginForm()
        context['form'] = form
        context['next'] = request.GET.get('next', 'main')
        return render(request, 'login_form.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            next = request.POST.get('next')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, 'Witaj, <b>{}</b>! {}'.format(username, Post.welcome()))
                request.session['welcome'] = True
                return redirect(next)
            else:
                messages.warning(request, 'Błędne dane logowania. Spróbuj jeszcze raz')
                context['form'] = form
                return render(request, 'login_form.html', context)
        else:
            messages.warning(request, 'formularz wypełniony niepoprawnie. Spróbuj jeszcze raz')
            context['form'] = form
            return render(request, 'login_form.html', context)
        return redirect('/')


class LogoutView(View):
    # simply logout action in react on press LOGOUT button
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.info(request, 'Użytkownik <b>{}</b> poprawnie wylogowany! {}'.format(username, Post.byebye()))
            request.session['welcome'] = False
        return redirect('/')


class CreateUserView(CreateView):
    # accet to CREATE USER form
    form_class = CreateUserForm
    template_name = 'create_user.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        try:
            context = super(CreateUserView, self).get_context_data(**kwargs)
            context.update({'submenu': Menu.getMenu('main'), 'title': 'dodawanie użytkownika'})
        except Exception as e:
            messages.warning(self.request, 'Błąd bazy danych: {}'.format(e))
        return context


class PasswordChangeView(LoginRequiredMixin, FormView):
    # access to CHANGE PASSWORD form
    form_class = PasswordChangeForm
    template_name = 'change_password.html'
    success_url = '/'
    # permission_required = 'auth.change_user'

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id).first()
        context.update({'submenu': Menu.getMenu('main'), 'title': 'Zmiana hasła', 'user': user})
        return context

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        user = User.objects.filter(id=user_id).first()
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(self.request, 'Pomyślna zmiana hasła dla {}!'.format(user.username))
        return super(PasswordChangeView, self).form_valid(form)

def PolitykaView(request):
    context['title'] = ''  # Polityka prywatności
    context['PB_Stories'] = []
    # context['logo'] = 'forum.png'
    return render(request, 'polityka.html', context=context)