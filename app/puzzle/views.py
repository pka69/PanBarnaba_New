'''
this view file serving view for select and solve puzzle
'''
from django.shortcuts import render

from main.models import Menu
from main.views import getBubbles


from .puzzle import puzzleList, puzzleSplited

context = {
    'submenu': Menu.getMenu('main')
}


def puzzleView(request):
    # view gives the user possibility to take a decision about picture to play
    context['puzzle'] = puzzleList('images/puzzle')
    context['title'] = ' Puzzle '
    context['PB_Stories'] = getBubbles(request)
    context['logo'] = 'puzzle.png'
    return render(request, 'puzzle/puzzle.html', context=context)


def puzzleSolve(request, puzzle_name):
    # view to play the puzzle
    level = int(request.COOKIES.get('level', '3'))
    context['puzzle'] = puzzle_name
    context['parts'] = puzzleSplited(puzzle_name, level)
    context['level'] = level
    context['rows'] = [item * level for item in range(level)]
    context['rowsend'] = [item * level + (level - 1) for item in range(level)]
    context['PB_Stories'] = getBubbles(request)
    context['logo'] = 'puzzle.png'
    return render(request, 'puzzle/puzzle_selected.html', context=context)