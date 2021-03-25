
from random import shuffle
from django.shortcuts import render

# Create your views here.

from django.views import View
from django.shortcuts import render

from main.models import Menu
from main.views import getBubbles

context = {}

GOL_STRUCTURE = {
    'Blinker': [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0],
        [0,1,1,1,0,0,1,0,0],
        [0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0],
        [0,1,1,1,0,0,1,0,0],
        [0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0],
    ],
    'froggy':[
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,1,1,0,0,0,1,1,1,0,0],
        [0,0,1,1,0,0,0,0,1,1,1,0],
        [0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0],
    ],
     'glider':[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ],
    'dakota':[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ],
     'crocodile':[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ],
    'fontaine':[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ],
    'breeder':[
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ],
}
GOL_REPEATER = {
    'Blinker': [False, False],
    'froggy': [False, False],
    'glider': [True, True],
    'dakota': [True, True],
    'crocodile': [False, False],
    'fontaine': [False, False],
    'breeder': [False, False],
}
class gameOfLifeView(View):
    def get(self, request):
        selected = list(GOL_STRUCTURE.keys())
        if actual:=request.GET.get('actual',''):
            step = int(request.GET['step'])
            actual_pos = selected.index(actual)
            if step==1:
                if actual_pos + 1 < len(selected):
                    actual_pos += 1
                else:
                    actual_pos = 0
            else:
                if actual_pos  == len(selected):
                    actual_pos += len(selected)-1
                else:
                    actual_pos -= 1
            selected = [selected[actual_pos]]
        else:
            shuffle(selected)
            selected = selected[:1]
        context['submenu'] = Menu.getMenu('main')
        context['title'] = 'Fascynyjący algorytm życia'
        # context['gols'] = [(item, range(len(GOL_STRUCTURE[item])*2), range(len(GOL_STRUCTURE[item][0])*2)) for item in selected]
        context['gols'] = [(item, range(len(GOL_STRUCTURE[item])), range(len(GOL_STRUCTURE[item][0]))) for item in selected]
        context['example'] =[GOL_STRUCTURE[item]  for item in selected]
        # context['rows'] = len(GOL_STRUCTURE[selected[0]]*2)
        # context['cols'] = len(GOL_STRUCTURE[selected[0]][0]*2)
        context['rows'] = len(GOL_STRUCTURE[selected[0]])
        context['cols'] = len(GOL_STRUCTURE[selected[0]][0])
        context['PB_Stories'] = getBubbles(request)
        context['repeater'] = GOL_REPEATER[selected[0]]
        context['logo'] = 'live.png'
        return render(request, 'maths/life.html', context=context)

class gameOfLifeGoView(View):
    def get(self, request):
        context['submenu'] = Menu.getMenu('main')
        context['title'] = 'Eksperymentuj z algorytmem życia'
        context['rows'] = 20
        context['cols'] = 50
        context['matrix'] = [range(context['rows']), range(context['cols'])]
        context['live'] = '23'
        context['born'] = '3'
        context['numbers'] = [str(item) for item in range(9)]
        context['generator'] = ['10%', '25%', '50%', '75%']
        context['speed'] = ['125', '250', '500', '1000']
        context['types'] = list(GOL_STRUCTURE.keys())
        context['PB_Stories'] = getBubbles(request)
        context['logo'] = 'live.png'
        return render(request, 'maths/life-go.html', context=context)

LABIRYNTH = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
    [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,],
    [1,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,],
    [1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,],
    [1,1,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,],
    [1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,1,1,1,1,],
    [1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,],
    [1,1,1,1,0,1,0,0,0,1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,],
    [1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,0,1,1,1,0,0,0,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,0,1,],
    [1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,1,1,0,1,],
    [1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,-2,],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,],
    [1,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,],
    [1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,],
    [1,1,1,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,],
    [1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,1,1,1,1,],
    [1,1,1,0,1,1,0,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,],
    [1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,],
    [1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
]
LABIRYNTH2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
    [1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,1,1,1,],
    [1,0,1,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,1,0,1,],
    [1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,0,-2,0,0,1,0,0,0,0,1,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,1,1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,0,1,],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,1,1,0,1,0,1,0,1,],
    [1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,],
    [1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,0,0,1,1,1,],
    [1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1,],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
]
class labirynthView(View):
    def get(self, request):
        context['submenu'] = Menu.getMenu('main')
        context['title'] = 'Jak komputer rozwiązuje labirynt?'
        context['rows'] = 20
        context['cols'] = 50
        context['labirynth'] = LABIRYNTH
        context['logo'] = 'labirynth.png'
        return render(request, 'maths/labirynth.html', context=context)

LAB_SIZE = [
    [20, 50],
    [40, 100],
    [10,25],
]

class labirynthGoView(View):
    def get(self, request, size= 0):
        context['submenu'] = Menu.getMenu('main')
        context['title'] = 'Zbuduj własny labirynt'
        context['rows'] = LAB_SIZE[size][0]
        context['cols'] = LAB_SIZE[size][1]
        context['matrix'] = [range(context['rows']), range(context['cols'])]
        context['speed'] = ['125', '250', '500', '1000']
        context['logo'] = 'labirynth.png'
        return render(request, 'maths/labirynth-go.html', context=context)


# brick icon https://www.onlinewebfonts.com/icon/568591