from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Question, Answer
from main.models import Menu
from main.views import getBubbles

context = {'submenu': Menu.getMenu('main')}


class quizListView(View):
    # select quiz set from a few groups (ease, medium, hard, extreme)
    def get(self, request):
        context['quiz_list'] = Question.groupList()
        context['title'] = 'wybierz zestaw'
        context['PB_Stories'] = getBubbles(request)
        context['logo'] = 'quiz.png'
        return render(request, 'quiz/quiz_list.html', context=context)


class quizPlayView(View):
    def get(self, request, qlevel, qgroup):
        quiz = Question.objects.filter(qlevel=qlevel, qgroup=qgroup).prefetch_related('answers')
        context['quiz'] = quiz
        context['level'] = 'level_{}'.format(qlevel)
        context['set_name'] = 'poziom {}, zestaw {}'.format(Question.LEVELS[qlevel][1], qgroup )
        context['qlevel'] = qlevel
        context['qgroup'] = qgroup
        context['PB_Stories'] = []
        context['logo'] = 'quiz.png'
        return render(request, 'quiz/quiz_play.html', context=context)

class quizNextView(View):
    def get(self, request, qlevel, qgroup):
        quiz_list = Question.groupList()
        temp = []
        for i in quiz_list:
            for j in i[1]:
                temp.append((i[2], j))
        act_quiz_position = temp.index((qlevel, int(qgroup))) + 1
        if act_quiz_position < len(temp):
            return redirect('/quiz/{}/{}'.format(temp[act_quiz_position][0],temp[act_quiz_position][1] ))
        messages.warning(request, 'Niestety, to już ostatni test dostępny na stronie. Postaramy się dołożyć wkrótce nowe wyzwania')
        return redirect('/quiz')

        return render(request, 'quiz/quiz_play.html', context=context)