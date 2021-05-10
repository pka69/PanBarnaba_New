from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):

    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

     # The below method returns all urls defined in urls.py file
    def items(self):
        return [
            'main',
            'contact',
            'info',
            'polityka',
            'login',
            'createuser',
            'posts:news',
            'posts:forum',
            'posts:bookpricelist',
            'posts:forum_rules',
            'maths:maths',
            'maths:game_of_life',
            'maths:labirynth',
            'moderate:moderate',
            'quiz:quiz_list',
            'puzzle:puzzle',
            'sudoku:sudoku',
            'memo:memo',
            'encrypt:mainEncrypt',
            'encrypt:friendMessageView',
            'differences:difference', 
        ]

    def location(self, item):
        return reverse(item)

from encrypt.encrypt import KEYS

class EncryptSitemap(Sitemap):
    changefreq = "never"
    priority = 0.0
    protocol = 'https'

    def items(self):
        return list(KEYS.keys())
        
    def location(self,item):
        return reverse('encrypt:specificEncrypt', kwargs={'action': item})
