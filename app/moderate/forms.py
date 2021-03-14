from django import forms

from quiz.models import Answer


class AnswerForm(forms.Form):
    # simply form for moderate module creating quiz answers
    answer = forms.CharField(label='wprowadź kolejną odpowiedź:', max_length=256)
    correct = forms.ChoiceField(label="czy to poprawna odpowiedź", initial=0, choices=((1, 'Tak'), (0, 'Nie')))