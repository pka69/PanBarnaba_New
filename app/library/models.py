from django.db import models


class Library(models.Model):
    area = models.CharField(max_length=32, default='', db_index=True)
    city = models.CharField(max_length=64, default='', db_index=True)
    name = models.CharField(max_length=255, default='')
    address1 = models.CharField(max_length=255, default='')
    address2 = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100, default='')
    moderator = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=100, default='')
    www = models.CharField(max_length=100, default='')
    salutation = models.CharField(max_length=50, default='')
    DDK_kids = models.BooleanField(db_index=True, default=False)
    DDK_adults = models.BooleanField(db_index=True, default=False)
    DDK_young = models.BooleanField(db_index=True, default=False)
    DDK_theme = models.CharField(max_length=30, default=False)
    notes = models.TextField(default='')
    closed = models.BooleanField(default=False)

    class Meta:
        db_table = "library"
        ordering = ['area',  'city']

    def __str__(self):
        return '{} - {}'.format(self.area, self.name) 