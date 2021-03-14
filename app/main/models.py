from django.db import models

# Create your models here.


class Menu(models.Model):
    '''
    table keep menu structure.
    '''
    group = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=30)
    picture = models.CharField(max_length=256, null=True)
    link = models.CharField(max_length=100)
    sub = models.CharField(max_length=30, default='', null=True)
    sequence = models.IntegerField(default=0)

    class Meta:
        unique_together = ('group', 'name')
        ordering = ['group',  'sequence', 'id']

    def save(self, *args, **kwargs):
        '''
        keep standard capitalise string unique field group and name 
        '''
        self.group = self.group.capitalize()
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.group, self.name)

    @classmethod
    def getMenu(cls, group, detail=0):
        '''
        generate list with menu. if SubMenu exist - it is included.
        if detail!=0 picture field is send back
        if any changes in menu model commena all bellow exept pass.
        '''
        pass
        menu = cls.objects.filter(group=group.capitalize())
        if detail:
            return [(
                item.name,
                item.picture,
                item.link,
                cls.getMenu(item.sub, detail) if item.sub else '') for item in menu]
        return [(
            item.name, 
            item.link, 
            cls.getMenu(item.sub, detail) if item.sub else '') for item in menu]