"""
"""
from math import sqrt
from random import choice


def CharCount(s, ava, out_type=0):
    """
    count repeating char in s
    out_type = 0 - return minimum repeating
    out_type = 1
    """
    s = sorted(s)
    # print(s)
    check = []
    for char in ava:
        no = s.count(char)
        check.append((char, no))
    if out_type == 0:
        return len([i for i in check if i[1] == 1])
    if out_type == 1:
        return ''.join([i[0] for i in check if i[1] == 1])
    if out_type == 2:
        return check
    if out_type == 3:
        pass


class Item:
    """
    main class of sudoku item
    x,y - coordinates in sudoku
    value - value of item
    fix_value - expected value
    fix - boolean, define the item with fixed value
    blocks - list of blocks (row, column, 3x3block) where this item is included
    hidden - bolean, for this items witch are not visible (in sudoku samurai)
    last_move - object collected the list of change in sudoku
    """

    def __init__(self, x=0, y=0, last_move=None, value='', hidden=False):
        self.__coord = (int(x), int(y))
        self.__blocks = []
        self.__hidden = bool(hidden)
        self.__last_move = last_move
        self.__value = str(value)
        if value:
            self.__fix_value = value
            self.__fix = True
        else:
            self.__fix_value = ''
            self.__fix = False

    def decopy(self):
        self.__fix = True
        if self.value:
            self.DelValue()
        self.SetValue(self.fix_value)

    @property
    def setcopy(self):
        if self.value:
            self.__fix_value = self.value
            self.__fix = True
            return True
        return False

    @property
    def fix(self):
        return self.__fix

    @property
    def value(self):
        return self.__value

    @property
    def coord(self):
        return self.__coord

    def AddRange(self, value):
        for block in self.blocks:
            block |= set(value)

    @property
    def compare(self):
        if self.hidden:
            return True
        return self.value == self.fix_value

    @property
    def fix_value(self):
        return self.__fix_value

    @property
    def hidden(self):
        return self.__hidden

    @property
    def DelValueWithFix(self):
        if self.value:
            self.DelValue()
            self.__fix = False

    @property
    def EmptyItem(self):
        return True if (not self.value and not self.hidden) else False

    @property
    def IsMove(self):
        if not self.value and not self.hidden:
            return self.GetRange()
        return False

    @property
    def NoMove(self):
        return not self.GetRange() if not self.hidden else False

    def AddBlock(self, block):
        self.blocks.append(block)

    @ property
    def blocks(self):
        return self.__blocks

    def __call__(self, value):
        self.DelValue()
        if value:
            return self.SetValue(value)

    def DelValue(self):
        if self.value == '':
            return False
        self.AddRange(self.value)
        self.__value = ''
        if self.__last_move:
            self.__last_move.DelHistory(self)
        return ''

    def CutRange(self, value):
        if not value:
            return
        for block in self.blocks:
            block -= set(value)

    def GetRange(self, string=False):
        if self.hidden or self.value:
            return '' if string else {}
        if len(self.blocks):
            r_value = ''
            ava = set(self.__blocks[0].GetRange)
            for block in self.blocks:
                r_value += block.ValuesStr()
                ava &= set(block.values)
        else:
            ava = set('123456789')
        if len(self.blocks) > 1:
            i = CharCount(r_value, ava, 1)
            if len(i) > 1:
                return '' if string else {}
            if len(i) == 1:
                return i if string else set(i)
        return ''.join(s for s in ava) if string else ava

    def SetValue(self, value, rnd=False):
        ava = self.GetRange()
        ok = True
        while ok:
            if not ava:
                return False
            if rnd:
                value = choice(list(ava))
            if not ((value) in (ava)):
                return False
            if self.__last_move and self.__last_move.CheckItem(self):
                return False
            if self.__last_move:
                self.__last_move.AddToHistory(self, value, ava)
            self.__value = value
            self.CutRange(value)
            if not rnd:
                return True
            itemlist = set()
            for block in self.blocks:
                itemlist = itemlist.union(set(block.items))
            itemlist.discard(self)
            if [item for item in itemlist if item.EmptyItem and item.NoMove]:
                ava -= set(value)
                self.DelValue()
                if len(ava) == 0:
                    return False
                continue
            while [item for item in itemlist if len(item.GetRange()) == 1]:
                select = [item for item in itemlist if len(item.GetRange()) == 1][0]
                if not select.SetValue("", True):
                    ava -= set(value)
                    self.DelValue()
                    if len(ava) == 0:
                        return False
                    break
            else:
                return True


class Block:
    def __init__(self, name, size=9, values='123456789'):
        self.__size = size
        self.__name = str(name)
        self.__values_range = values
        self.__values = {values[c] for c in range(size)}
        self.__items = []

    def __isub__(self, value):
        self.__values = self.__values - set(value)

    def __ior__(self, value):
        self.__values = self.__values | set(value)

    @property
    def size(self):
        return self.__size

    @property
    def values(self):
        if self.__values != self.CheckValues():
            pass
        return self.__values

    def CheckValues(self):
        check = {self.__values_range[c] for c in range(self.__size)}
        for item in self.items:
            check -= set(item.value)
        return check

    def AddItem(self, item):
        if len(self.__items) == self.__size:
            return False
        v = item.value
        if v and set(v) & self.values == {}:
            return False
        self.__items.append(item)
        self.__values |= set(v)
        item.AddBlock(self)
        return True

    @property
    def name(self):
        return self.__name

    @property
    def items(self):
        return self.__items

    @property
    def GetRange(self):
        return self.__values_range

    def ValuesStr(self):
        return ''.join(s for s in self.values) if len(self.values) else ''

    def CreateItems(self, rnd=True, line=False):
        if line:
            for i, val in enumerate(sorted(list(self.__values))):
                item = Item(0, i, None, val, False)
                self.AddItem(item)
            return
        temp_values = sorted(list(self.__values))
        size = int(sqrt(self.__size))
        for i in range(size):
            for j in range(size):
                item = Item(i, j, None, temp_values[i * size + j], False)
                self.AddItem(item)