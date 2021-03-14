from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


from django.db import IntegrityError, DatabaseError
from django.core.mail import send_mail, mail_admins
from django.conf import settings

from posts.models import Post


BOOK = 5  # posty type for pricelist in Post model

URL = 'https://lubimyczytac.pl/ksiazka/4958750/pan-barnaba-i-zagadkowa-hipoteza'  # url adress

CSS_SELECTORS = {
    'book_type': 'body > div.content > main > div > div:nth-child(8) > div:nth-child(1) > div.col-md-8 > section > nav',
    'papierowe': '#bb_książka',
    'ebook': '#bb_ebook',
    'allformats': '#bb_wszystkie',
    'promoted': '#buybox-bookstores-promoted > div',
    'other': '#buybox-bookstores',  # #buybox-bookstores > div
    'bookstorename': ' div.bookstore-name',
    'bookstorekind': 'div.bookstore-item-kind',
    'bookstoreprice': ' div.bookstore-item-price > div',
    'showall': '#buybox-show-all',
    'acceptcookies': '#onetrust-accept-btn-handler',
    'tomove': 'body > div.content > main > div > div:nth-child(9) > div:nth-child(1) > div.col-md-8 > div ',
    'tomove2': 'body > div.content > main > div > div:nth-child(8) > div:nth-child(1) > div.col-md-8 > div',

}  # dictionary with specific selectors


def bsAnalyzer(book_store):
    """
    for specific elementh on lubimyczytac.pl lokking for detail:
        bookstore_name,
        bookstore_icon,
        bookstore_href,
        book_kind,
        book_price,
    """
    try:
        bookstore_name = book_store.find_element_by_css_selector(CSS_SELECTORS['bookstorename'])
        bookstore_kind = book_store.find_element_by_css_selector(CSS_SELECTORS['bookstorekind'])
        bookstore_price = book_store.find_element_by_css_selector(CSS_SELECTORS['bookstoreprice'])
    except NoSuchElementException:
        return False
    temp = bookstore_price.text.split('\n')
    if len(temp) == 2:
        bookstore_price = temp[0].replace(',', '.')
    if len(temp) == 3:
        bookstore_price = temp[1].replace(',', '.')
    return {
        'bookstore_name': bookstore_name.text,
        'bookstore_icon': bookstore_name.find_element_by_css_selector('img').get_attribute('src'),
        'bookstore_href': book_store.get_attribute('href'),
        'book_kind': bookstore_kind.text,
        'book_price': bookstore_price,
    }


def openURL():
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install())
    webaddress = URL
    print('otwieram', URL)
    driver.get(webaddress)
    driver.fullscreen_window()
    driver.find_element_by_css_selector(CSS_SELECTORS['acceptcookies']).send_keys(Keys.ENTER)
    try:
        temp = driver.find_element_by_css_selector(CSS_SELECTORS['tomove'])
    except NoSuchElementException:
        temp = driver.find_element_by_css_selector(CSS_SELECTORS['tomove2'])
    hover = ActionChains(driver)
    hover.move_to_element(temp)
    hover.perform()
    hover.click(on_element=temp)
    hover.perform()
    book_stores = []
    temp = driver.find_element_by_css_selector(CSS_SELECTORS['allformats'])
    hover = ActionChains(driver)
    hover.move_to_element(temp)
    hover.perform()
    hover.click(on_element=temp)
    hover.perform()
    try:
        temp = driver.find_element_by_css_selector(CSS_SELECTORS['showall'])
    except NoSuchElementException:
        pass
    else:
        hover = ActionChains(driver)
        hover.move_to_element(temp)
        hover.perform()
        hover.click(on_element=temp)
        hover.perform()
    book_stores = []
    try:
        promoted_book_store_list = driver.find_element_by_css_selector(CSS_SELECTORS['promoted'])
        other_book_store_list = driver.find_element_by_css_selector(CSS_SELECTORS['other'])
    except NoSuchElementException:
        driver.close()
        driver.quit
        return False
    for book_store in promoted_book_store_list.find_elements_by_css_selector('a'):
        temp = bsAnalyzer(book_store)
        if temp and temp['bookstore_name']:
            print('zczytano {}'.format(temp['bookstore_name']))
            book_stores.append(temp)
    for book_store in other_book_store_list.find_elements_by_css_selector('a'):
        temp = bsAnalyzer(book_store)
        if temp and temp['bookstore_name']:
            print('zczytano {}'.format(temp['bookstore_name']))
            book_stores.append(temp)
    for item in book_stores:
        webaddress = item['bookstore_href']
        driver.get(webaddress)
        item['bookstore_href'] = driver.current_url
        if item['bookstore_name'].lower().startswith('legimi'):
            print('legime price change')
            price = driver.find_element_by_css_selector('#react-app > div > div > section > div > div.options-tab-scroll-content.col-xs-12.col-md-9 > div > ul > li:nth-child(2) > p')
            print('legime price change', price.text)
            price = float(price.text.split(' ')[-2].replace(',', '.'))
            item['book_price'] = price
    driver.close()
    driver.quit
    return book_stores


def loadBookPrices():
    # test passage
    # print('testing send_mail')
    # print('email host', settings.EMAIL_HOST)
    # print('email port', settings.EMAIL_PORT)
    # print('email user', settings.EMAIL_HOST_USER)
    # print('email pass', settings.EMAIL_HOST_PASSWORD)
    # print('email default', settings.DEFAULT_FROM_EMAIL)
    # print('email SSL', settings.EMAIL_USE_SSL)
    # print('email TSL', settings.EMAIL_USE_TLS)
    # send_mail(
    #     'zaimportowano ceny',
    #     'z sukcesem zaimportowano 0 cen z lubimyczytac.pl',
    #     from_email=settings.DEFAULT_FROM_EMAIL, 
    #     recipient_list=['pjkalista@gmail.com'],
    #     fail_silently=False
    # )
    # print('testing mail_admins')
    # mail_admins('błąd importu cen','wystapił bład w trakcie importu cen z lubimyczytac.pl',fail_silently=False)
    # return 0
    # test finished
    try:
        book_price_list = openURL()
    except Exception as e:
        mail_admins('błąd importu cen','wystapił bład w trakcie importu cen z lubimyczytac.pl\nkoniecznie sprawdzić!',fail_silently=True)
        return False
    if book_price_list:
        print('usuwam stare ceny')
        Post.objects.filter(group=BOOK).delete()
        print('ceny usunięte')
    else:
        mail_admins('brak cen','import cen z lubimyczytac.pl zwrócił zerową listę.\n Sprawdzić przyczynę.',fail_silently=True)
        return False
    posts = []
    for book in book_price_list:
        posts.append(
            Post(
                group=BOOK,
                subgroup=book['book_kind'],
                content=book['bookstore_name'],
                picture=book['bookstore_icon'],
                stage=1,
                external_link=book['bookstore_href'],
                dec_content=float(book['book_price']),
            )
        )
    try:
        Post.objects.bulk_create(posts)
    except DatabaseError as e:
        print('błąd bazy danych', e)
        mail_admins('błąd bazy danych','Przy próbie dodawania nowych cen.\n Sprawdzić!!!',fail_silently=True)
        return False
    except IntegrityError as e:
        print('błąd integralności danych danych', e)
        mail_admins('błąd bazy danych','Problem spójności bazy danych',fail_silently=True)
        return False
    print('zapisano {} cen'.format(len(posts)))
    msg = '\n'.join([
        '{:10} {:20} - {:>6}'.format(
            book['book_kind'],
            book['bookstore_name'],
            book['book_price']
        ) for book in book_price_list
    ])
    print(msg)
    msg = 'z sukcesem zaimportowano {} cen z lubimyczytac.pl'.format(len(book_price_list)) + '\n' + msg
    mail_admins(
        'zaimportowano ceny',
        msg,
        fail_silently=True
    )
    return len(book_price_list)