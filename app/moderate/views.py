'''
this part of website is only for users with can_moderate permission.
Main functionality:
 * adding post other than forum posts,
 * buid quiz structure
'''
import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Count, Q
from django.views import View
from django.db import IntegrityError, DatabaseError
from django.conf import settings



from posts.models import Post, STAGE, POST_TYPE
from main.models import Menu
from quiz.models import Question, Answer
from .forms import AnswerForm
from library.models import Library
from tools.mail import mail_to_DKK

MAIL_LAYOUT = [
    "DKK_invitation",
    "Konkurs_1",
    "Konkurs_2",
]

PAGE_RECORDS = 20
PERMISSION = 'posts.moderate'
ACTION = {
    'reject': -1,
    'approve': 1,
}
context = {'submenu': Menu.getMenu('moderate')} 


def paginate(qs_list, page=1):
    '''
    funkcja zwracająca obiekt paginacji dla wyświetlanych danych
    '''
    paginator = Paginator(qs_list, PAGE_RECORDS)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result


@permission_required(PERMISSION)
def moderateView(request, post_type=2, action=None, id=None):
    '''
    show varius types of posts (types definied in posts.models Post.POST_TYPE)
    moderator can accept ore rejects posts from user forum.
    moderator can add various posts like news, content, notes, quotation
    '''
    if request.method == 'POST':
        post_id = request.POST.get('id','')
        if post_id:  # if post_id is empty, than create a new post, else modify existing post
            post = Post.moderate.get(id=int(post_id))
        else:
            post = Post()
            post.owner = request.user
        post.subgroup = request.POST.get('subgroup', '')
        post.group = int(request.POST.get('group', 0))
        post.content = request.POST.get('content', '')
        post.stage = int(request.POST.get('stage', ''))
        if post.stage == 1:
            post.moderator = request.user
        post.external_link = request.POST.get('external_link', '')
        picture = ''
        if request.POST.get('pictureType', '') == '1':
            post.picture = request.POST.get('picture', '')
        else:
            picture = request.FILES.get('pictureFile', None)
        if picture:
            mypath = settings.DEPLOY_ROOT / 'images/posts'
            filename = picture.name
            full_name = os.path.join(mypath, filename)
            open(full_name, 'wb').write(picture.file.read()) 
            post.picture = '/images/posts/' + filename
        post.save()
        if post_id:
            messages.success(request, 'Post został zaktualizowany')
        else:
            messages.success(request, 'Post został dodany')
        
    if action in ACTION.keys():
        post = Post.moderate.get(id=id)
        post.stage = ACTION[action]
        post.moderator = request.user
        post.save()
        messages.success(request, 'Akcja {} zakończona sukcesem'.format(action))
    sfiltr = request.GET.get("sfiltr",'')
    stagelist = request.GET.getlist("stagelist", [stage[0] for stage in STAGE])
    posts = Post.moderate.filter(group=post_type).filter(stage__in=stagelist)
    if sfiltr:
        posts = posts.filter(
            Q(subgroup__icontains=sfiltr) | Q(content__icontains=sfiltr)
        )
    posts = posts.order_by('group', 'subgroup','-p_date', '-p_time')
    for i in range(len(stagelist)): stagelist[i] = int(stagelist[i])
    page = int(request.GET.get('page', 1))
    context['posts'] = paginate(posts, page)
    context['STAGE'] = STAGE
    context['post_type_selected'] = POST_TYPE[post_type]
    context['stagelist'] = stagelist
    context['post_type'] = POST_TYPE
    context['sfiltr'] = sfiltr
    context['title'] = 'zarządzanie treścią'
    return render(request, 'moderate/moderate.html', context=context)

@permission_required(PERMISSION)
def quizView(request, level=None):
    '''
    this view shows list of all questions and based on modal form allow to create anothe one and skip
    to next view when moderator can built answers structure
    '''
    if request.method == 'POST':
        quiz_id = request.POST.get('id','')
        if quiz_id:  # if post_id is empty, than create a new post, else modify existing post
            quiz = Question.objects.get(id=int(quiz_id))
        else:
            quiz = Question()
            quiz.owner = request.user
        quiz.qgroup = request.POST.get('qgroup', '')
        request.session['qgroup'] = quiz.qgroup
        quiz.qlevel = int(request.POST.get('qlevel', 0))
        request.session['qlevel'] = quiz.qlevel
        quiz.question = request.POST.get('question', '')
        quiz.qtype = int(request.POST.get('qtype', 0))
        try:
            quiz.save()
        except IntegrityError as e:
            messages.error(request, 'akcja nieudana. {}'.format(e))
        except DatabaseError as e:
            messages.error(request, 'akcja nieudana. {}'.format(e))
        else:
            messages.success(request, 'Zapisano pytanie: '.format(quiz.question))
            return redirect('/moderate/quiz_answers/{}'.format(quiz.id))
    if level:
        quiz_list = Question.objects.filter(qlevel=level).annotate(ans=Count('answers'))
    else:
        quiz_list = Question.objects.annotate(ans=Count('answers'))
    context['submenu'] = Menu.getMenu('moderate')
    context['quiz_list'] = quiz_list
    context['qlevels'] = Question.LEVELS
    context['qtypes'] = Question.TYPES
    context['title'] = 'sekcja budowania quizu'
    context['default_qgroup'] = request.session.get('qgroup', '')
    context['default_qlevel'] = request.session.get('qlevel', None)
    return render(request, 'moderate/quiz.html', context=context)

class quizQuestionDelete(PermissionRequiredMixin, View):
    '''
    this view delete selected question with relate answers
    '''
    permission_required = (PERMISSION)
    def get(self, request, id, level=None):
        Question.objects.filter(id=id).delete()
        messages.success(request, 'usunięto 1 pytanie')
        redirect_url = '/moderate/quiz/{}/'.format(id)
        return redirect(redirect_url)


class quizAnswerDelete(PermissionRequiredMixin, View):
    '''
    this view is action on press trash on question question answer recors
    '''
    permission_required = (PERMISSION)
    def get(self, request, id, item_id):
        Answer.objects.filter(id=item_id).delete()
        messages.success(request, 'usunięto 1 odpowiedź')
        redirect_url = '/moderate/quiz_answers/{}/'.format(id)
        return redirect(redirect_url)


class quizDetailView(PermissionRequiredMixin, View):
    '''
    this view give an access to build a structure of correct/incorrect answers
    '''
    permission_required = (PERMISSION)
    def get(self, request, id):
        quiz = Question.objects.get(id=id)
        form = AnswerForm()
        context['submenu'] = Menu.getMenu('moderate')
        context['quiz'] = quiz
        context['answers'] = Answer.objects.filter(quiz=quiz)
        context['form'] = form
        return render(request, 'moderate/quiz_answers.html', context=context)

    def post(self, request, id):
        form = AnswerForm(request.POST)
        quiz = Question.objects.get(id=id)
        if quiz.qtype == 0:
            can_be_true = not quiz.answers.filter(correct=True).count()
        else:
            can_be_true = True
        if form.is_valid():
            answer = form.cleaned_data['answer']
            correct = True if form.cleaned_data['correct'] == '1' else False
            if (not can_be_true) and correct:
                messages.error(request, 'może byc tylko jend prawidłowa odpowiedź')
            else:
                try:
                    item = Answer.objects.create(quiz=quiz, answer=answer, correct=correct)
                except IntegrityError as e:
                    messages.error(request, 'akcja nieudana. {}'.format(e))
                except DatabaseError as e:
                    messages.error(request, 'akcja nieudana. {}'.format(e))
                else:
                    messages.success(request, 'dodano {} odpowiedź'.format('poprawną' if correct else 'błędną'))
        return self.get(request, id)

class libraryListView(PermissionRequiredMixin, View):
    permission_required = (PERMISSION)
    def post(self, request):
        next = request.get_full_path()
        lib_data = {}
        id = request.POST.get('id','')
        lib_data['moderator'] = request.POST.get('moderator','')
        lib_data['email'] = request.POST.get('email','')
        lib_data['www'] = request.POST.get('www','')
        lib_data['telefon'] = request.POST.get('telefon','')
        lib_data['salutation'] = request.POST.get('salutation','')
        lib_data['notes'] = request.POST.get('notes','')
        lib_data['name'] = request.POST.get('name','')
        lib_data['city'] = request.POST.get('city','')
        lib_data['ddk_theme'] = request.POST.get('theme','')
        lib_data['ddk_kids'] = True if request.POST.get('ddk_kids','') else False
        lib_data['ddk_young'] = True if request.POST.get('ddk_young','') else False
        lib_data['ddk_adults'] = True if request.POST.get('ddk_adults','') else False
        lib_data['closed'] = True if request.POST.get('ddk_closed','') else False
        library = Library.objects.filter(id=id)[0]
        for key, value in lib_data.items():
            setattr(library, key, value)
            # library[key] = value
        library.save()
        return redirect(next)

    def get(self, request):
        libraries = Library.objects.all()
        context['max_lib'] = libraries.count()
        if not int(request.GET.get('page', 0)):
            area_filtr = request.GET.get('area_filtr','')
            request.session['area_filtr'] = area_filtr
            name_filtr = request.GET.get('name_filtr', '')
            request.session['name_filtr'] = name_filtr
            email_filtr = request.GET.get('email_filtr', '')
            request.session['email_filtr'] = email_filtr
            moderator_filtr = request.GET.get('moderator_filtr', '')
            request.session['moderator_filtr'] = moderator_filtr
            kids = request.GET.get('kids', False)
            adults = request.GET.get('adults', False)
            young = request.GET.get('young', False)
            closed = request.GET.get('closed', False)
            request.session['kids'] = kids
            request.session['adults'] = adults
            request.session['young'] = young
            request.session['closed'] = closed
        else:
            area_filtr = request.session.get('area_filtr','')
            name_filtr = request.session.get('name_filtr','')
            email_filtr = request.session.get('email_filtr','')
            moderator_filtr = request.session.get('moderator_filtr','')
            kids = request.session.get('kids',False)
            adults = request.session.get('adults',False)
            young = request.session.get('young',False)
            closed = request.session.get('closed',False)
        if area_filtr:
            libraries = libraries.filter(area__icontains=area_filtr)
        if kids:
            libraries = libraries.filter(DDK_kids=True)
        if adults:
            libraries = libraries.filter(DDK_adults=True)
        if young:
            libraries = libraries.filter(DDK_young=True)
        if closed:
            libraries = libraries.filter(closed=True)
        if name_filtr:
            libraries = libraries.filter(
                Q(city__icontains=name_filtr) |
                Q(name__icontains=name_filtr) 
            )
        if moderator_filtr:
            libraries = libraries.filter(moderator__icontains=moderator_filtr) 
        request.session['email_filtr'] = email_filtr
        if email_filtr:
            libraries = libraries.filter(email__icontains=email_filtr)    
        page = int(request.GET.get('page', 1))
        context['libraries'] = paginate(libraries, page)
        context['area_filtr'] = area_filtr
        context['name_filtr'] = name_filtr
        context['moderator_filtr'] = moderator_filtr
        context['email_filtr'] = email_filtr
        context['kids'] = kids
        context['adults'] = adults
        context['young'] = young
        context['closed'] = closed
        context['title'] = 'Lista DKK'
        context['submenu'] = Menu.getMenu('moderate')
        context['akt_lib'] = libraries.count()
        context['mail'] = MAIL_LAYOUT
        context['url_next'] = request.get_full_path()
        return render(request, 'moderate/libraries.html', context=context)


def libraryMailSend(request, template, n1, n2):
    area_filtr = request.GET.get('area_filtr','')
    name_filtr = request.GET.get('name_filtr', '')
    email_filtr = request.GET.get('email_filtr', '')
    moderator_filtr = request.GET.get('moderator_filtr', '')
    kids = request.GET.get('kids', False)
    adults = request.GET.get('adults', False)
    young = request.GET.get('young', False)
    closed = request.GET.get('closed', False)
    libraries = Library.objects.all()
    filtr_end = '&'
    if area_filtr:
        libraries = libraries.filter(area__icontains=area_filtr)
    if kids:
        libraries = libraries.filter(DDK_kids=True)
        filtr_end +="kids=on"
    if adults:
        libraries = libraries.filter(DDK_adults=True)
        filtr_end +="adults=on"
    if young:
        libraries = libraries.filter(DDK_young=True)
        filtr_end +="young=on"
    if closed:
        libraries = libraries.filter(closed=True)
        filtr_end +="closed=on"
    if name_filtr:
        libraries = libraries.filter(
            Q(city__icontains=name_filtr) |
            Q(name=name_filtr) 
        )
    if moderator_filtr:
        libraries = libraries.filter(moderator__icontains=moderator_filtr) 
    request.session['email_filtr'] = email_filtr
    if email_filtr:
        libraries = libraries.filter(email__icontains=email_filtr)   
    libraries = libraries.exclude(email__isnull=True)    
    if len(filtr_end) == 1: 
        filtr_end = ''
    mail_to_DKK(template, libraries, False)
    messages.success(request, 'wysłano wiadomość {} do {} DKK'.format(template, libraries.count()))
    return redirect('/moderate/library_list/?area_filtr={}&name_filtr={}&moderator_filtr={}&email_filtr={}{}'.format(
        area_filtr, name_filtr, moderator_filtr, email_filtr, filtr_end
    ))