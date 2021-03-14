'''
various view of different types of posts:
    * bookstore prices
    * news
    * forum
'''
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  # to delete in final project
from django.contrib.auth.mixins import LoginRequiredMixin # to delete in final project


from main.models import Menu
from main.views import getBubblesLike, getBubbles
from moderate.views import paginate
from .models import Post

PAGE_RECORDS = 20
FTYPES = ('o książce', 'o stronie', 'do autorki', 'pomysły na kontynuację', 'Hyde Park', 'FanFiki')

context = {'submenu': Menu.getMenu('main')}

@login_required(redirect_field_name='my_redirect_field')  # to delete in final project
def bookstorePricesView(request, subgroup=''):
    # show last bookstore prices (updated every day)
    # if subgroup:
    #     context['bookstoreprices'] = Post.bookBestPrice(booktype=subgroup, only_one=False)
    # else:
    #     context['bookstoreprices'] = Post.bookBestPrice(only_one=False)
    context['title'] = 'Ceny w ksiegarniach'
    # context['lastupdate'] = Post.lastPriceDate().strftime("%Y/%m/%d")
    # context['booktypes'] = Post.bookTypes()
    context['PB_Stories'] = getBubbles(request)
    return render(request, 'posts/bookstore_prices.html', context=context)

@login_required(redirect_field_name='my_redirect_field')  # to delete in final project
def newsView(request):
    # show nes posted by moderators
    page = int(request.GET.get('page', 1))
    context['posts'] = paginate(Post.notRejected.filter(group=0), page)
    context['title'] = 'Poznaj ostatnie wieści'
    context['PB_Stories'] = getBubbles(request)
    return render(request, 'posts/posts_list.html', context=context)


class forumView(LoginRequiredMixin, View):
    login_url = '/login/'  # to delete in final project
    redirect_field_name = 'my_redirect_field'  # to delete in final project

    # view for show user forum with a few categories
    def get(self, request, ftype=FTYPES[0]):
        page = int(request.GET.get('page', 1))
        context['title'] = 'zapraszamy na forum Pana Barnaby'
        context['ftypes'] = FTYPES
        context['ftype'] = ftype
        context['posts'] = paginate(Post.approved.filter(group=2).filter(subgroup=ftype).filter(related_post__isnull=True).prefetch_related('comments'), page)
        context['PB_Stories'] = getBubblesLike(request)
        return render(request, 'posts/forum_list.html', context=context)
  
    # post post from forum or alternatively comments
    def post(self, request, ftype=FTYPES[0]):
        post_id = request.POST.get('post_id', None)
        user_id = request.POST.get('user', 0)
        subgroup = request.POST.get("subgroup", 0)
        content = request.POST.get("content", 0)
        external_link = request.POST.get("external_link", '')
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            messages.error(request, 'Wystąpił błąd. Aby wstawić post trzeba być zalogowanym')
            return redirect('/posts/forum/{}'.format(ftype))
        if post_id:
            Post.objects.create(group=2,
                subgroup=subgroup,
                content=content,
                external_link=external_link,
                owner=user
            )
        else:
            Post.objects.create(
                group=2,
                subgroup=subgroup,
                content=content,
                external_link=external_link,
                owner=user
            )
        messages.success(request, 'Wpis został przekazany moderatorom do akceptacji')
        return redirect('/posts/forum/{}'.format(ftype))


class forumReactView(View):
    def get_post(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, react, ftype=FTYPES[0], post_id=0):
        post = self.get_post(post_id)
        try:
            user = User.objects.get(pk=request.user.id)
        except User.DoesNotExist:
            raise Http404
        if post.owner.id == user.id:
            return JsonResponse({"status": "error", "comment": "reaction '{}' for post {} - it's your post!".format(react, post_id)})
        if react == 'positives':
            if user not in post.positives.all():
                if user in post.negatives.all():
                    post.negatives.remove(user)
                    post.positives.add(user)
                    return JsonResponse({"status": "change", "comment":  "reaction '{}' for post {} changed".format(react, post_id)})
                post.positives.add(user)
            else:
                return JsonResponse({"status": "error", "comment": "reaction '{}' for post {} already exist".format(react, post_id)})
        elif react == 'negatives':
            if user not in post.negatives.all():
                if user in post.positives.all():
                    post.positives.remove(user)
                    post.negatives.add(user)
                    return JsonResponse({"status": "change", "comment":  "reaction '{}' for post {} changed".format(react, post_id)})
                post.negatives.add(user)
            else:
                return JsonResponse({"status": "error", "comment":  "reaction '{}' for post {} already exist".format(react, post_id)})
        return JsonResponse({"status": "success", "comment":  "reaction '{}' for post {} added".format(react, post_id)})
