from django.db import IntegrityError, DatabaseError

from main.models import Menu

Menu_details = (
    {'group': 'main', 'name': 'zagrajmy', 'link': '/games/', 'sequence': '10'},
    {'group': 'main', 'name': 'ciekawostki', 'link': '/maths/', 'sequence': '20'},
    {'group': 'main', 'name': 'forum', 'link': '/posts/forum/', 'sequence': '30'},
    {'group': 'main', 'name': 'o autorce', 'link': '/info/#author', 'sequence': '40'},
    {'group': 'main', 'name': 'inne', 'link': '', 'sub':'info', 'sequence': '50'},
    {'group': 'info', 'name': 'kontakt', 'link': '/contact/', 'sequence': '10'},
    {'group': 'info', 'name': 'wieści', 'link': '/posts/news/', 'sequence': '20'},
    {'group': 'info', 'name': 'o książkach', 'link': '/info/#books', 'sequence': '30'},
    {'group': 'info', 'name': 'gdzie kupić', 'link': '/posts/bookpricelist/', 'sequence': '40'},
     {'group': 'info', 'name': 'regulamin forum', 'link': '/posts/rules/', 'sequence': '50'},
    {'group': 'games', 'name': 'quiz', 'picture':'quiz.png', 'link': '/quiz/', 'sequence': '10'},
    {'group': 'games', 'name': 'puzzle', 'picture': 'puzzle.png', 'link': '/puzzle/', 'sequence': '20'},
    {'group': 'games', 'name': 'sudoku', 'picture':'sudoku.png', 'link': '/sudoku/', 'sequence': '30'},
    {'group': 'games', 'name': 'szyfrowanie', 'picture':'encrypt.png', 'link': '/encrypt/', 'sequence': '40'},
    {'group': 'games', 'name': 'znajdź różnicę', 'picture': 'difference.png', 'link': '/difference/', 'sequence': '50'},
    {'group': 'games', 'name': 'memo', 'picture': 'memo.png', 'link': '/memo/', 'sequence': '60'},
    {'group': 'maths', 'name': 'algorytm życia', 'picture':'live.png', 'link': '/maths/life/', 'sequence': '10'},
    {'group': 'maths', 'name': 'świat fractali', 'picture':'fractal.png', 'link': '/maths/fractals/', 'sequence': '20'},
    {'group': 'maths', 'name': 'zaprojektuj labirynt', 'picture':'labirynth.png', 'link': '/maths/labirynth/', 'sequence': '30'},
    {'group': 'moderate', 'name': 'moderacja postów', 'link': '', 'sub': 'posts', 'sequence': '10'},
    {'group': 'moderate', 'name': 'QUIZ - zadania ', 'link': '/moderate/quiz/', 'sequence': '20'},
    {'group': 'moderate', 'name': 'Lista bibliotek DKK ', 'link': '/moderate/library_list/', 'sequence': '30'},
    {'group': 'posts', 'name': 'News', 'link': '/moderate/0/', 'sequence': '10'},
    {'group': 'posts', 'name': 'Quotation', 'link': '/moderate/1/', 'sequence': '20'},
    {'group': 'posts', 'name': 'Forum', 'link': '/moderate/2/', 'sequence': '30'},
    {'group': 'posts', 'name': 'Notes', 'link': '/moderate/3/', 'sequence': '40'},
    {'group': 'posts', 'name': 'Post', 'link': '/moderate/4/', 'sequence': '50'},
    # {'group': 'posts', 'name': 'BookPrice', 'link': '/moderate/5/', 'sequence': '10'},
    {'group': 'posts', 'name': 'Content', 'link': '/moderate/6/', 'sequence': '60'},
    {'group': 'posts', 'name': 'Message', 'link': '/moderate/7/', 'sequence': '70'},
    {'group': 'posts', 'name': 'Welcome', 'link': '/moderate/8/', 'sequence': '80'},
    {'group': 'encrypt', 'name': 'GA-DE-RY-PO-LU-KI', 'picture':'gaderypoluki.png', 'link': '/encrypt/gaderypoluki/', 'sequence': '10'},
    {'group': 'encrypt', 'name': 'CZEKOLADKA', 'picture':'czekoladka.png', 'link': '/encrypt/brownie/', 'sequence': '20'},
    {'group': 'encrypt', 'name': 'UŁAMKOWY', 'picture':'ulamkowy.png', 'link': '/encrypt/divider/', 'sequence': '30'},
    {'group': 'encrypt', 'name': 'KACZOR', 'picture':'kaczor.png', 'link': '/encrypt/kaczor/', 'sequence': '40'},
)


def create_menu():
    '''
    create menu elements based on dict Menu_details
    '''
    for item in Menu_details:
        try:
            Menu.objects.create(**item)
        except IntegrityError as e:
            print('Błąd bazy dlanych ', e, ' dla zestawu: {} \n'.format(item))
        except DatabaseError as e:
            print('Błąd bazy dlanych ', e, ' dla zestawu: {} \n'.format(item))
    
def update_menu_picture():
    for item in Menu_details:
        if item.get('picture'):
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(picture=item['picture'])
        else:
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(picture='')

def new_compare():
    item = {'group': 'games', 'name': 'znajdź różnicę', 'picture': 'difference.png', 'link': '/difference/'}
    try:
        Menu.objects.create(**item)
    except IntegrityError as e:
        print('Błąd bazy danych ', e, '\ndla zestawu: {}'.format(item))
    except DatabaseError as e:
        print('Błąd bazy danych ', e, '\ndla zestawu: {}'.format(item))


def update_menu_links():
    for item in Menu_details:
        if item.get('link'):
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(link=item['link'])
        else:
            Menu.objects.filter(group=item['group'].capitalize()).filter(name=item['name'].capitalize()).update(link='')

def refresh_menu():
    Menu.objects.all().delete()
    create_menu()