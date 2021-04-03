from datetime import time

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist

from .models import Score
# Create your views here.


def scoreCheckView(request, game, game_id, s_result, hours, minutes, seconds):
    s_time = time(hour=hours, minute=minutes, second=seconds)
    s_result = round(float(s_result))  # if s_result[-1] == '%' else int(s_result)
    try:
        user = User.objects.get(pk=request.user.pk)
        user_result = Score.objects.filter(game=game).filter(game_id=game_id).filter(user=user).first()
    except ObjectDoesNotExist:  # EmptyResultSet
        user = None
        user_result = None
    position, total_players, game_results = Score.checkResultPosition(game, game_id, s_result, s_time)
    message = '''Brawo! <br>
    Twój wynik {}%  w {} daje Ci {} miejsce wśród {} osób, które w to grały!<br>
    '''.format(s_result, s_time.strftime("%H:%M:%S") ,position, total_players)
    if user:
        if user_result:
            if (s_result > user_result.s_result) or (
                (s_result == user_result.s_result) and (s_time < user_result.s_time)
            ):
                message = message + '<br>Udało Ci sie poprawić swój poprzedni wynik!'
    else:
        message = message + '<br>Żeby być widocznym w rankingu trzeba założyc konto.'
    result = {
        'status': "success",
        'message': message, 
        'records': total_players,
        'top':game_results
    }
    return JsonResponse(result)


def scoreUpdateView(request, game, game_id, s_result, hours, minutes, seconds):
    s_time = time(hour=hours, minute=minutes, second=seconds)
    s_result = int(s_result[:-1]) if s_result[-1] == '%' else int(s_result)
    try:
        user = User.objects.get(pk=request.user.pk)
        user_result = Score.objects.filter(game=game).filter(game_id=game_id).filter(user=user).first()
    except ObjectDoesNotExist:  # EmptyResultSet
        return JsonResponse({'status': 'error', 'message': 'nie jesteś zalogowany. <br> Zaloguj sie lub załóż konto'})
    if not user_result:
        user_result = Score(user=user, game=game, game_id=game_id)
    user_result.s_result = s_result
    user_result.s_time = s_time
    try:
        user_result.save()
        message = 'Wynik użytkownika {} został zapisany'.format(user.username)
        status = "success"
    except Exception as e:
        message = e
        status = 'error'
    position, total_players, game_results = Score.checkResultPosition(game, game_id, s_result, s_time)
    result = {
        'status': status,
        'message': message, 
        'records': total_players,
        'top': game_results
    }
    return JsonResponse(result)
    