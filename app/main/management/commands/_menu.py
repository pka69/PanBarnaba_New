from django.db import IntegrityError, DatabaseError

from main.models import Menu

Menu_details = (
    {'group': 'main', 'name': 'zagrajmy', 'link': '/games/'},
    {'group': 'main', 'name': 'chcesz wiedzieć?', 'link': '/maths/'},
    {'group': 'main', 'name': 'forum', 'link': '/posts/forum/'},
    {'group': 'main', 'name': 'informacje', 'link': '', 'sub':'info'},
    {'group': 'main', 'name': 'kontakt', 'link': '/contact/'},
    {'group': 'info', 'name': 'o autorce', 'link': '/info/#author'},
    {'group': 'info', 'name': 'o książkach', 'link': '/info/#books'},
    {'group': 'info', 'name': 'wieści', 'link': '/posts/news/'},
    {'group': 'info', 'name': 'gdzie kupić', 'link': '/posts/bookpricelist/'},
    {'group': 'games', 'name': 'quiz', 'picture':'quiz.png', 'link': '/quiz/'},
    {'group': 'games', 'name': 'puzzle', 'picture': 'puzzle.png', 'link': '/puzzle/'},
    {'group': 'games', 'name': 'sudoku', 'picture':'sudoku.png', 'link': '/sudoku/'},
    {'group': 'games', 'name': 'szyfrowanie', 'picture':'encrypt.png', 'link': '/encrypt/'},
    {'group': 'maths', 'name': 'algorytm życia', 'picture':'live.png', 'link': '/maths/life/'},
    {'group': 'maths', 'name': 'świat fractali', 'picture':'fractal.png', 'link': '/maths/fractals/'},
    {'group': 'maths', 'name': 'zaprojektuj labirynt', 'picture':'labirynth.png', 'link': '/maths/labirynth/'},
    {'group': 'moderate', 'name': 'moderacja postów', 'link': '', 'sub': 'posts'},
    {'group': 'moderate', 'name': 'QUIZ - zadania ', 'link': '/moderate/quiz/'},
    {'group': 'posts', 'name': 'News', 'link': '/moderate/0/'},
    {'group': 'posts', 'name': 'Quotation', 'link': '/moderate/1/'},
    {'group': 'posts', 'name': 'Forum', 'link': '/moderate/2/'},
    {'group': 'posts', 'name': 'Notes', 'link': '/moderate/3/'},
    {'group': 'posts', 'name': 'Post', 'link': '/moderate/4/'},
    {'group': 'posts', 'name': 'BookPrice', 'link': '/moderate/5/'},
    {'group': 'posts', 'name': 'Content', 'link': '/moderate/5/'},
    {'group': 'encrypt', 'name': 'GA-DE-RY-PO-LU-KI', 'picture':'gaderypoluki.png', 'link': '/encrypt/gaderypoluki/'},
    {'group': 'encrypt', 'name': 'CZEKOLADKA', 'picture':'czekoladka.png', 'link': '/encrypt/brownie/'},
    {'group': 'encrypt', 'name': 'UŁAMKOWY', 'picture':'ulamkowy.png', 'link': '/encrypt/divider/'},
    {'group': 'encrypt', 'name': 'KACZOR', 'picture':'kaczor.png', 'link': '/encrypt/kaczor/'},
)


def create_menu():
    '''
    create menu elements based on dict Menu_details
    '''
    for item in Menu_details:
        try:
            Menu.objects.create(**item)
        except IntegrityError as e:
            print('Błąd bazy dlanych ', e, '\ndla zestawu: {}'.format(item))
        except DatabaseError as e:
            print('Błąd bazy dlanych ', e, '\ndla zestawu: {}'.format(item))
    
def update_menu_picture():
    for item in Menu_details:
        if item.get('picture'):
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(picture=item['picture'])
        else:
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(picture='')