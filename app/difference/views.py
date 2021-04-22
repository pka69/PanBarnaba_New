'''
this view file serving view for select and solve puzzle
'''
from django.shortcuts import render

from main.models import Menu
from main.views import getBubbles


from puzzle.puzzle import puzzleList, puzzleListContain

context = {
    'submenu': Menu.getMenu('main')
}


def differenceView(request):
    # view gives the user possibility to take a decision about picture to play
    picture_list = puzzleList('images/difference')
    context['difference'] = [(item[0], item[1], item[2].replace("puzzle","difference")) for item in  picture_list]
    context['title'] = ' Znajdź różnicę'
    context['PB_Stories'] = getBubbles(request)
    context['logo'] = 'difference.png'
    return render(request, 'difference/difference.html', context=context)


def differenceSolve(request, picture_name):
    # view to play the difference
    level = 3  # int(request.COOKIES.get('level', '3'))
    file_name = picture_name.split('.')
    parts = puzzleListContain('images/difference/diff', file_name[0])
    parts_det = parts[0][0].split('_')
    blocksize = int(parts_det[1])
    diff_list = [['' for i in range(blocksize)] for j in range(blocksize)]
    for diff in parts:
            parts_det = diff[0].split('_')
            diff_list[int(parts_det[3])][int(parts_det[2])] = diff[1]
    diff_counter = 0
    for i in range(blocksize):
        for j in range(blocksize):
            if type(diff_list[i][j]) == str and len(diff_list[i][j]):
                if i > 0 and type(diff_list[i-1][j]) == tuple:
                    diff_list[i][j] = (diff_list[i][j], diff_list[i-1][j][1])
                elif j > 0 and type(diff_list[i][j-1]) == tuple:
                    diff_list[i][j] = (diff_list[i][j], diff_list[i][j-1][1])
                else:
                    diff_counter += 1
                    diff_list[i][j] = (diff_list[i][j], diff_counter)
    for i in range(blocksize):
        for j in range(blocksize):
            if type(diff_list[i][j]) == str: continue
            if i + 1 < blocksize and type(diff_list[i+1][j]) == tuple:
                if diff_list[i+1][j][1] < diff_list[i][j][1]:
                    for k in range(blocksize):
                        for l in range(blocksize):
                            if type(diff_list[k][l]) == tuple and diff_list[k][l][1] > diff_list[i][j][1]:
                                diff_list[k][l] = (diff_list[k][l][0], diff_list[k][l][1] - 1)
                    diff_list[i][j] = (diff_list[i][j][0], diff_list[i][j+1][1])
            if j + 1 < blocksize and type(diff_list[i][j+1]) == tuple:
                if diff_list[i][j+1][1] < diff_list[i][j][1]:
                    for k in range(blocksize):
                        for l in range(blocksize):
                            if type(diff_list[k][l]) == tuple and diff_list[k][l][1] > diff_list[i][j][1]:
                                diff_list[k][l] = (diff_list[k][l][0], diff_list[k][l][1] - 1)
                    diff_list[i][j] = (diff_list[i][j][0], diff_list[i][j+1][1])
                
    context['diff_list'] = diff_list
    context['difference'] = picture_name
    context['level'] = level
    context['PB_Stories'] = getBubbles(request)
    context['blocksize'] = blocksize
    context['logo'] = 'difference.png'
    return render(request, 'difference/difference_selected.html', context=context)