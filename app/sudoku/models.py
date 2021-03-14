from django.db import models


# Create your models here.

class Cell(models.Model):
    # model of single cell in Sudoku
    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField(default=0)
    border = models.CharField(max_length=5)
    fix = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    sudoku = models.ForeignKey('Sudoku', related_name='cells', on_delete=models.CASCADE, null=True)
    blocks = models.ManyToManyField('Block', related_name='cells')

    class Meta:
        ordering = ['x', 'y']

    def __str__(self):
        return '({:2},{:2})  - ({}). ({}) ({})'.format(
            self.x, self.y, self.value,
            'hiden' if self.hidden else '',
            'fixed' if self.fix else '',
        )


class Block(models.Model):
    # block model join together cells 
    name = models.CharField(max_length=10)
    sudoku = models.ForeignKey('Sudoku', related_name='blocks', on_delete=models.CASCADE, null=True)


class Sudoku(models.Model):
    #model sudoku collecting all cells and all blocks 
    slug = models.TextField(db_index=True, unique=True)
    level = models.CharField(max_length=20)
    size = models.IntegerField()

    @property
    def result(self):
        return ''.join(str(item.value) for item in self.cells.all())