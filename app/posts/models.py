import datetime

from django.db import models
from django.contrib.auth.models import User

from random import choice

# Create your models here.

POST_TYPE = (
    (0, 'News'),  # newses from internet
    (1, 'Quotation'),  # quotation from books
    (2, 'Forum'),   # users forum
    (3, 'Notes'),  # notes from author
    (4, 'Post'),  # special post for website
    (5, 'BookPrice'),  # price monitoring book
    (6, 'Content'),  # website content
    (7, 'Message'),  # message from users
    (8, 'Welcome'), # WelcomeMessage
    # (9, 'Nie używać!!!'),
    # (10, 'Regulations'),
)

STAGE = (
    (0, 'posted'),
    (1, 'approved'),
    (-1, 'rejected'),
    (2, 'main view post')

)
SHORT = 20

class ApprovedManager(models.Manager):
    use_for_related_fields = True
    def get_queryset(self): 
        return super().get_queryset().filter(stage=1)

class MainViewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stage=2)

class NotRejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stage__in=[0,1])

class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(stage=-1)

class Post(models.Model):
    group = models.IntegerField(choices=POST_TYPE, db_index=True, verbose_name='grupa')
    subgroup = models.CharField(max_length=64, default='', db_index=True, verbose_name='podgrupa')
    p_date = models.DateField(auto_now_add=True, db_index=True, verbose_name='data')
    p_time = models.TimeField(auto_now_add=True, db_index=True, verbose_name='godzina')
    stage = models.IntegerField(choices=STAGE, db_index=True, default=0, verbose_name='status')
    owner = models.ForeignKey(User, default=None, null=True, related_name='set_posts', on_delete=models.SET_DEFAULT, db_index=True, verbose_name='właściciel')
    moderator = models.ForeignKey(User, default=None, null=True, related_name='set_moderation', on_delete=models.SET_DEFAULT, db_index=True, verbose_name='moderator')
    content = models.TextField(default='', verbose_name='treść')
    dec_content = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='wartość', null=True)
    external_link = models.URLField(default='', max_length=500, verbose_name='link')
    picture = models.CharField(default='', max_length=350, verbose_name='obrazek')
    related_post = models.ForeignKey('Post', related_name="comments", default=None, null=True, on_delete=models.CASCADE, verbose_name='post nadrzędny')
    positives = models.ManyToManyField(User, related_name="positive_reaction", default=None, verbose_name='pozytywne')
    negatives = models.ManyToManyField(User, related_name="negative_reaction", default=None, verbose_name='pozytywne')
    objects = ApprovedManager()
    approved = ApprovedManager()
    notRejected = NotRejectedManager()
    mainPost = MainViewManager()
    moderate = models.Manager()
    rejected = RejectedManager()

    class Meta:
        ordering = ['-p_date', '-p_time']
        permissions = (
            ("moderate", "Can moderate posts"),
        )

    def __str__(self):
        return "id: {},data: {} {} - {}".format(self.id, self.p_date, self.get_group_display(), self.content[:20])

    def export(self):
        return {
            'group': self.group, 
            'subgroup': self.subgroup, 
            'content': self.content, 
            'dec_content': self.dec_content,
            'external_link': self.external_link,
            'picture': self.picture
        } 
    @property
    def content_html(self):
        return self.content.replace("\n", "<br>")
        
    @property
    # return date and time together
    def fulldate(self):
        return datetime.datetime.combine(self.p_date, self.p_time)

    @property
    def short_link(self):
        if len(self.external_link) < SHORT:
            return self.external_link
        return self.external_link[:(SHORT // 2 - 2)] + '...' + self.external_link[-(SHORT // 2 - 1):]

    @property
    def short_picture(self):
        if len(self.picture) < SHORT:
            return self.picture
        return self.picture[:(SHORT // 2 - 2)] + '...' + self.picture[-(SHORT // 2 - 1):]
    # @classmethod
    # # return last date for specific post types
    # def lastPriceDate(cls, group=5):
    #     return cls.objects.filter(group=group).first().p_date

    # @classmethod
    # # return best or all book prices 
    # def bookBestPrice(cls, booktype=None, only_one=True):
    #     pricelist = cls.objects.filter(group=5).order_by('dec_content')
    #     if booktype:
    #         pricelist = pricelist.filter(subgroup=booktype)
    #     if only_one:
    #         pricelist = pricelist.first()
    #     return pricelist

    # @classmethod
    # # return book types
    # def bookTypes(cls):
    #     return cls.objects.filter(group=5).order_by('subgroup').distinct('subgroup').values_list('subgroup', flat=True)

    @classmethod
    def welcome(cls):
        return choice(cls.notRejected.filter(group=8).filter(subgroup='in')).content

    @classmethod
    def byebye(cls):
        return choice(cls.notRejected.filter(group=8).filter(subgroup='out')).content