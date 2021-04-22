from random import shuffle

from django.shortcuts import render

from main.models import Menu
from main.views import getBubbles
from puzzle.puzzle import puzzleList

# Create your views here.

context = {
    'submenu': Menu.getMenu('main')
}

def memoView(request):
    context['title'] = 'Memo'
    context['PB_Stories'] = getBubbles(request)
    context['logo'] = 'difference.png'
    return render(request, 'memo/memo.html', context=context)

def memoSolveView(request, level = 4):
    parts = puzzleList('images/memo', True)[:(level * level // 2)]
    parts.extend(parts)
    shuffle(parts)
    memos = []
    for i in range(level):
        memos.append([])
        for j in range(level):
            memos[i].append(parts[i * level + j][1])
    context['memos'] = memos
    context['PanBarnaba'] = 'images/lapka.png'
    context['title'] = 'Memo'
    context['PB_Stories'] = getBubbles(request)
    context['level'] = level
    context['logo'] = 'difference.png'
    return render(request, 'memo/memo_selected.html', context=context)
