from os import listdir
from os.path import isfile, join
from random import choice, shuffle

from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.staticfiles.templatetags.staticfiles import static, do_static
from django.templatetags.static import static
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import get_files



from tools.block import Block


class PuzzleBlock(Block):
    # class defined for shuffle picture parts
    def __init__(self, size, fname):
        self.block_size = size
        name = fname.split('.')
        super().__init__(
            "Puzzle",
            size * size,
            ['{}_({})_{}_{}.{}'.format(name[0], size, i, j, name[1]) for i in range(size) for j in range(size)])
        self.CreateItems(False, False)
        self.emptyitem = self.items[size * size - 1]

    def Move(self, dy, dx):
        x, y = self.emptyitem.coord
        x += dx
        y += dy
        space = list(range(self.block_size))
        if x in space:
            if y in space:
                item = self.items[x * self.block_size + y]
                val = item.value
                item('')
                self.emptyitem(val)
                item(" ")
                self.emptyitem = item
                print()
                print(self)

    def Shuffle(self):
        last_move = (0, 0)
        while True:
            for i in range(100):
                move = choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
                while move == last_move:
                    move = choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
                self.Move(move[0], move[1])
                last_move = (-move[0], -move[1])
            if sum([item.compare for item in self.items]) == 0:
                return

    @property
    def compare(self):
        return sum([item.compare for item in self.items]) == len(self.items)


def puzzleList(location, make_shuffle=False):
    # list of pictures in static/images/puzzle directory

    # s = StaticFilesStorage()
    # list(get_files(s, location=location))

    mypath = settings.STATICFILES_DIRS[0] /  location  if settings.STATIC_ROOT == '' else settings.STATIC_ROOT /  location# static(location) 
    allfiles = [
        (
            f.split('.')[0],
            f,
            'puzzle_selected/{}'.format(f)) for f in listdir(mypath) if isfile(join(mypath, f))]
    shuffle(allfiles)       
    return allfiles if make_shuffle else sorted(allfiles)

def puzzleListContain(location, mask):
    # list of pictures in static/images/puzzle directory


    # s = StaticFilesStorage()
    # list(get_files(s, location=location))

    mypath = settings.STATICFILES_DIRS[0] /  location  if settings.STATIC_ROOT == '' else settings.STATIC_ROOT /  location# static(location) 
    allfiles = [
        (
            f.split('.')[0],
            f,
            'puzzle_selected/{}'.format(f)) for f in listdir(mypath) if isfile(join(mypath, f)) and f.find(mask) > -1]
    return sorted(allfiles)

def puzzleSplited(fname, level):
    # based on defined level define the picture parts name 
    new_puzzle = PuzzleBlock(level, fname)
    new_puzzle.Shuffle()
    allfiles = [[item.value, item.fix_value] for item in new_puzzle.items]
    return allfiles