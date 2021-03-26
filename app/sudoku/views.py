from random import choice

from django.shortcuts import render
from django import views

from .models import Cell, Sudoku
from main.models import Menu
from main.views import getBubbles

# Create your views here.

context = {
    'submenu': Menu.getMenu('main')
}


def sudokuSelectView(request):
    # show three types of sudoku
    sudoku = [
        ['mini (4x4)', 'sudoku-4.png', '/sudoku/4'],
        ['standard (9x9)', 'sudoku-9.png', '/sudoku/9'],
        ['Samurai', 'sudoku-samurai.png', '/sudoku/Samurai'],
    ]
    context['sudoku'] = sudoku
    context['title'] = ' Sudoku '
    context['PB_Stories'] = getBubbles(request)
    context['logo'] = 'sudoku.png'
    return render(request, 'sudoku/sudoku.html', context=context)


class sudokuGameView(views.View):
    # choice sudoku frm database and prepare data for game
    def get(self, request, sudoku_type):
        sudoku_list = Sudoku.objects.filter(level=sudoku_type)
        sudoku = choice(sudoku_list) if sudoku_list else None
        items = Cell.objects.filter(sudoku=sudoku).order_by('x', 'y').prefetch_related("blocks")
        context['items'] = items
        context['level'] = sudoku.level
        context['size'] = sudoku.size - 1
        context['numbers'] = [item + 1 for item in range(min(9, sudoku.size))]
        context['slug'] = sudoku.result
        context['logo'] = 'sudoku.png'
        context['PB_Stories'] = []
        return render(request, 'sudoku/sudoku_selected.html', context=context)