# this program generate the sudoku table with various dimension
from random import choice, shuffle  # biblioteka generatora losowego
from math import sqrt
# from SudokuMasterGrid import matrix_variation


class SudItem:
    def __init__(self, x, y, last_move=None, value='', hidden=False, decor=''):
        self.__coord = (int(x), int(y))
        self.__value = str(value)
        self.__fix_value = ''
        self.__fix = False
        self.__blocks = []
        self.__hidden = bool(hidden)
        self.__decor = decor
        self.__last_move = last_move

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
    def fix_value(self):
        return self.__fix_value

    @property
    def fix(self):
        if self.__hidden:
            return True
        return self.__fix

    @property
    def DelValueWithFix(self):
        if self.value:
            self.DelValue()
            self.__fix = False

    @property
    def compare(self):
        if self.hidden:
            return True
        return self.value == self.fix_value

    def __iter__(self):
        return (i for i in (self.coord, self.value, self.blocks, self.hidden, self.decor, self.SetValue, self.fix))

    def __repr__(self):
        class_name = type(self).__name__
        return '{} coord:{}, value: "{}", block: {}, hidden: {}, decor: "{}"'.format(class_name, *self)

    def __str__(self):
        return (
            "coord: {}, value: '{}', blocks: {}, hidden: {}, decor: '{}'".format(
                self.coord,
                self.value,
                len(self.blocks),
                self.hidden,
                self.decor,
            )
        )

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

    @property
    def blocks(self):
        return self.__blocks

    def GetRange(self, str=False):
        ava = set('123456789')
        if self.hidden or self.value:
            return '' if str else {}
        if len(self.blocks) != 0:
            r_value = ''
            for block in self.blocks:
                r_value += block.ValuesStr()
                ava &= set(block.values)
            for i in ava:
                if r_value.count(i) == 1:
                    return str(i) if str else i
        return ''.join(s for s in ava) if str else ava

    def GetRangeIf(self):
        if not self.value:
            return self.GetRange()
        s = self.value
        self.DelValue()
        r = self.GetRange()
        self.SetValue(s)
        return r

    def CutRange(self, value):
        if not value:
            return
        for block in self.blocks:
            block -= set(value)

    def AddRange(self, value):
        for block in self.blocks:
            block |= set(value)

    def SetRandomValue(self):
        ava = self.GetRange()
        if not ava:
            return False
        return self.SetValue(choice(list(ava)))

    @property
    def coord(self):
        return self.__coord

    @property
    def x(self):
        return self.__coord[0]

    @property
    def y(self):
        return self.__coord[1]

    @property
    def value(self):
        return self.__value

    def SetValue(self, value):
        ava = self.GetRange()
        if not ((value) in (ava)):
            return False
        if self.__last_move.CheckItem(self):
            return False
        self.__last_move.AddToHistory(self, value, ava)
        self.__value = value
        self.CutRange(value)
        return True

    def DelValue(self):
        self.AddRange(self.value)
        self.__value = ''
        self.__last_move.DelHistory(self)
        return True

    @property
    def decor(self):
        return self.__decor

    def SetDecor(self, decor):
        self.__decor = decor

    @property
    def hidden(self):
        return self.__hidden

    def __call__(self, value):
        if not value and self.value:
            return self.DelValue()
        else:
            return self.SetValue(value)


class LastMove:
    def __init__(self):
        self.__item_list = []
        self.__value_list = []

    def AddToHistory(self, item, value, value_set):
        if self.__item_list.count(item) > 0:
            return False
        self.__item_list.insert(0, item)
        self.__value_list.insert(0, (value, len(value_set)))
        return True

    def CheckItem(self, item):
        return bool(self.__item_list.count(item))

    def DelHistory(self, item):
        if not self.__item_list.count(item):
            return False
        i = self.__item_list.index(item)
        self.__item_list.pop(i)
        self.__value_list.pop(i)
        return True

    def DelLast(self, no=1):
        if not len(self.__item_list):
            return
        for _ in range(no):
            self.__item_list.pop(0)
            self.__value_list.pop(0)

    @property
    def size(self):
        return len(self.__item_list)

    @property
    def lastitem(self):
        if not len(self.__item_list):
            return list()
        return self.__item_list[0], self.__value_list[0][0], self.__value_list[0][1]

    def DelHistoryAll(self):
        self.__item_list.clear()
        self.__value_list.clear()


class SudBlock:
    def __init__(self, name, size=9, decor=True, values='123456789'):
        self.__size = size
        self.__name = str(name)
        self.__values = {values[c] for c in range(size)}
        self.__items = []
        if decor:
            s = int(sqrt(size))
            self.__decor = []
            TB = "T" + " " * (s - 2) + "B"
            LR = "L" + " " * (s - 2) + "R"
            for i in range(s):
                for j in range(s):
                    self.__decor.append((TB[i] + LR[j]).replace(" ", ""))
        else:
            self.__decor = False

    @property
    def name(self):
        return self.__name

    def AddItem(self, item):
        if len(self.__items) == self.__size:
            return False
        v = item.value
        if v and set(v) & self.values == {}:
            return False
        self.__items.append(item)
        item.AddBlock(self)
        if self.__decor:
            item.SetDecor(self.__decor[len(self.__items) - 1])
        self |= set(v)

    @property
    def items(self):
        return self.__items
    # -------------do przemyślenia---------------

    def SetItems(self):
        if not len(self.values):
            return True
        counter = 1
        while [item for item in self.items if item.EmptyItem]:
            if not self.GetOnlyOne():
                item = choice(
                    [item for item in self.items if item.value == ''])
                if item.NoMove:
                    self.ClearAll()
                    counter += 1
                    continue
                val = choice(list(item.GetRange()))
                if not item(val):
                    self.ClearAll()
            else:
                val = self.GetOnlyOne()
                item = val[0]
                if not item(val[1]):
                    self.ClearAll()
                    counter += 1
            if counter == 20:
                return False
        return True

    @property
    def values(self):
        return self.__values

    def ValuesStr(self):
        return ''.join(s for s in self.values) if len(self.values) else ''

    def GetName(self):
        return self.__name

    def GetOnlyOne(self):
        pos = []
        pos.extend([(item, item.GetRange(True))
                    for item in self.items if len(item.GetRange()) == 1])
        return pos[0] if len(pos) else pos

    def ClearAll(self):
        for item in self.items:
            if item.value:
                item('')

    def __isub__(self, value):
        self.__values = self.__values - set(value)

    def __ior__(self, value):
        self.__values = self.__values | set(value)


class Sudoku:
    def __init__(self, type=9, sub_samurai=None, parent=None, last_move=None):
        self.items = []
        self.blocks = []
        self.type = type
        self.last_move = LastMove()
        self.sub = []
        if parent:
            self.parent = parent
            self.last_move = last_move

        def blocksindex(name, _type, _hidden):
            ind = list(filter(lambda bl: bl.GetName() == name, self.blocks))
            if len(ind):
                return ind[0]
            bl = SudBlock(name, _type, _hidden)
            self.blocks.append(bl)
            return bl

        if sub_samurai:
            x, y = [[6, 6], [0, 12], [0, 0], [12, 0], [12, 12]][sub_samurai - 1]
            for item in parent.items:
                if item.coord[0] in range(x, x + 9) and item.coord[1] in range(y, y + 9):
                    self.items.append(item)
                    for bl in item.blocks:
                        if not len(list(filter(lambda block: block.GetName() == bl.GetName(), self.blocks))):
                            self.blocks.append(bl)
                    row = blocksindex(str(sub_samurai) + "row_" + str(item.coord[0]), type, False)
                    col = blocksindex(str(sub_samurai) + "col_" + str(item.coord[1]), type, False)
                    row.AddItem(item)
                    col.AddItem(item)
                    if parent.blocks.count(row) == 0:
                        parent.blocks.append(row)
                    if parent.blocks.count(col) == 0:
                        parent.blocks.append(col)
            return
        if type == 4 or type == 9:
            s = int(sqrt(type))
            for i in range(type):
                b1 = i // s
                row = (SudBlock("row_" + str(i), type, False))
                self.blocks.append(row)
                for j in range(type):
                    b2 = j // s
                    col = blocksindex("col_" + str(j), type, False)
                    block = blocksindex(
                        "block_" + str(b1) + "_" + str(b2), type, True)
                    item = SudItem(i, j, self.last_move)
                    self.items.append(item)
                    row.AddItem(item)
                    col.AddItem(item)
                    block.AddItem(item)
        elif type == "Samurai":
            self.type = 21
            s = 3
            hidden_block = ['30', '31', '03', '13', '53', '63', '35', '36']
            for i in range(self.type):
                b1 = i // s
                for j in range(self.type):
                    b2 = j // s
                    hidden = bool(hidden_block.count(str(b1) + str(b2)))
                    item = SudItem(i, j, self.last_move, '', hidden)
                    self.items.append(item)
                    if not hidden:
                        block = blocksindex(
                            "block_" + str(b1) + "_" + str(b2), 9, not hidden)
                        block.AddItem(item)
            for i in range(1, 6):
                self.sub.append(Sudoku(9, i, self, self.last_move))

    def __str__(self):
        box = [['L', 0, -1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['║', '║', '╬', '╠', '╣', '╠', '╣', '╠', '╣', '╬', '╬', '╬']],
               ['R', 0, 1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['║', '║', '╬', '╠', '╣', '╠', '╣', '╠', '╣', '╬', '╬', '╬']],
               ['T', -1, 0, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['══', '╬', '══', '╦', '╦', '╩', '╩', '╬', '╬', '╦', '╩', '╬']],
               ['B', 1, 0, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['══', '╬', '══', '╦', '╦', '╩', '╩', '╬', '╬', '╦', '╩', '╬']],
               ['TL', -1, -1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['╔', '╠', '╦', '╔', '╦', '╠', '╬', '╠', '╬', '╦', '╬', '╬']],
               ['TR', -1, 1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['╗', '╣', '╦', '╦', '╗', '╬', '╣', '╬', '╣', '╦', '╬', '╬']],
               ['BR', 1, 1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['╝', '╣', '╩', '╬', '╗', '╬', '╣', '╬', '╣', '╦', '╬', '╬']],
               ['BL', 1, -1, ['', '║', '══', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬'],
                ['╚', '╠', '╩', '╠', '╣', '╚', '╩', '╠', '╬', '╬', '╩', '╬']]
               ]
        output = []
        output = [[''] * (self.type * 2 + 1) for i in range(self.type * 2 + 1)]

        for i in range(1, self.type * 2 + 1, 2):
            for j in range(1, self.type * 2 + 1, 2):
                item = self.items[i // 2 * self.type + j // 2]
                decor = item.decor
                output[i][j] = item.value.ljust(2)
                if decor != "":
                    for k in range(8):
                        if box[k][0] in decor:
                            cell = output[i + box[k][1]][j + box[k][2]]
                            output[i + box[k][1]][j + box[k][2]] = box[k][4][box[k][3].index(cell.replace(' ', ''))]
                if item.hidden:
                    output[i - 1][j] = output[i - 1][j].ljust(2)
                    output[i + 1][j] = output[i + 1][j].ljust(2)
                    if j < 5:
                        output[i][j] = '   '
        s = ''
        for i in range(self.type * 2 + 1):
            r = ''.join(str(output[i][j]) for j in range(self.type * 2 + 1))
            if len(r) and (len(r) != r.count(' ')):
                s = s + r + '\n'
        return s

    def SetDiagonal(self, reverse=False):
        if any(item.fix for item in self.items if not item.hidden):
            return
        if self.sub:
            i = 0
            for s in self.sub:
                i += 1
                s.SetDiagonal(not (i % 2))
            return
        temp_block = [block for block in self.blocks if block.GetName().count(
            '_') == 2 and block.values]
        for block in temp_block:
            sek = block.GetName().split('_')
            if reverse:
                sek[1] = str(6 - int(sek[1]))
            if (int(sek[1]) % 4) == (int(sek[2]) % 4):
                i = 0
                while [item for item in block.items if item.EmptyItem]:
                    block.SetItems()
                    while len(list(item for item in self.items if item.EmptyItem and item.NoMove)) != 0:
                        block.ClearAll()

    def SetSudValues(self):
        break_flag = False
        empty_items = []
        only_one_items = {}

        def updateEmptyItems():
            nonlocal empty_items
            empty_items = list(filter(lambda item: item.EmptyItem, self.items))

        def clearIfNoMove():
            nonlocal empty_items
            while [item for item in empty_items if item.NoMove]:
                last_item = self.last_move.lastitem
                while last_item[2] <= int(sqrt(self.type)):
                    item = last_item[0]
                    if item(''):
                        empty_items.append(item)
                    last_item = self.last_move.lastitem
                if self.last_move.size < 2:
                    return
                for _ in range(2):
                    last_item = self.last_move.lastitem
                    item = last_item[0]
                    if item(''):
                        empty_items.append(item)

        def updateOnlyOne():
            nonlocal only_one_items, break_flag, empty_items
            only_one_items = [(item, item.GetRange(True))
                              for item in empty_items if len(item.GetRange()) == 1]
            break_flag = bool([(item, item.GetRange())
                               for item in empty_items if item.NoMove])

        if len(self.sub) > 0:
            for s in self.sub:
                s.SetSudValues()
                print(self)
            return True
        self.SetDiagonal()
        updateEmptyItems()
        while len(empty_items) > 0 and not break_flag:
            clearIfNoMove()
            updateOnlyOne()
            while len(only_one_items) > 0 and not break_flag:
                item = only_one_items[0][0]
                if item(str(only_one_items[0][1])):
                    empty_items.pop(empty_items.index(item))
                    updateOnlyOne()
                else:
                    break_flag = True
            if len(empty_items) != 0 and not break_flag:
                item = choice(empty_items)
                if item.SetRandomValue():
                    empty_items.pop(empty_items.index(item))
                else:
                    break_flag = True
                    self.last_move.DelLast()
            if break_flag:
                clearIfNoMove()
                break_flag = False
        self.last_move.DelHistoryAll()
        return True

    def SolvePuzzle(self, reverse=False):
        empty_items = []

        def sort_key_range(item):
            return len(item.GetRange())

        def SolveItem(no, reverse):
            nonlocal empty_items
            item = empty_items[no]
            s = item.GetRange(str)
            if len(s) == 0:
                return False
            if reverse:
                s = s[::-1]
            for i in range(len(s)):
                if item(s[i]):
                    if [item for item in self.items if (item.EmptyItem and item.NoMove)]:
                        continue
                    if len(empty_items) == no + 1:
                        return True
                    if SolveItem(no + 1, reverse):
                        return True if item.compare else False
                item('')
            return False
        empty_items = [item for item in self.items if item.EmptyItem]
        empty_items.sort(key=sort_key_range)
        return SolveItem(0, reverse)

    def SetPuzzle(self, level='E'):

        def sort_key_range_if(item):
            return len(item.GetRangeIf())

        changed = []
        temp_item_list = []
        temp_block = []
        steps = []
        temp_block = [
            block for block in self.blocks if block.GetName().count('_') == 2]
        block_no = len(temp_block)
        all = len([item for item in self.items if not item.hidden])
        steps = [1] * (all)
        if self.type == 4:
            steps[0] = 8
        elif self.type == 9:
            steps[0] = 18
            steps[1] = 9
        elif self.type == 21:
            steps[0] = 82
            steps[1] = 41
        while True:
            [item.setcopy for item in self.items]
            counter = 0
            for step in steps:
                corr = False
                temp_item_list = [
                    item for item in self.items if not item.EmptyItem]
                shuffle(temp_item_list)
                temp_item_list.sort(key=sort_key_range_if)
                for temp_pos in range(len(temp_item_list) + 1):
                    counter += 1
                    if temp_pos == len(temp_item_list):
                        print('zerwanie pętli')
                        temp_item_list = [
                            item for item in self.items if item.EmptyItem]
                        print('usunięto ', len(temp_item_list), ' komórek')
                        # [item.decopy() for item in temp_item_list]
                        # print(self)
                        return
                    if (step) >= block_no:
                        temp_block.reverse()
                    for bl in range(step):
                        if (step) >= block_no:
                            temp_item_list = [
                                item for item in temp_block[bl % block_no].items if not item.EmptyItem]
                            shuffle(temp_item_list)
                        changed.append(temp_item_list[temp_pos])
                        temp_item_list[temp_pos].DelValueWithFix
                    for k in range(2):
                        corr = self.SolvePuzzle(bool(k))
                        [item('') for item in self.items if not item.fix]
                        if not corr:
                            [item.decopy() for item in changed]
                            self.last_move.DelHistoryAll()
                            break
                    changed.clear()
                    if corr:
                        break
                i = len([item for item in self.items if not item.fix])
                print('krok {}: usunięto {} komórek'.format(counter, i))
                print(self)
            print('zakończono')
            temp_item_list = list(
                item for item in self.items if item.EmptyItem)
            i = len(temp_item_list)
            print('usunięto ', i, ' komórek')
            return
            # for item in temp_item_list:
            #     item.decopy()
            # print(self)

    def Slug(self):
        return ''.join([item.fix_value for item in self.items])


"""
------------- main program --------------------------------
"""
if __name__ == "__main__":
    new_sud_small = Sudoku(4)
    new_sud_small.SetDiagonal()
    print(new_sud_small)
    new_sud_small.SetSudValues()
    print(new_sud_small)
    new_sud_small.SetPuzzle()

    new_sudoku = Sudoku(9)
    new_sudoku.SetDiagonal()
    print(new_sudoku)
    new_sudoku.SetSudValues()
    print(new_sudoku)
    new_sudoku.SetPuzzle()

    new_Samurai = Sudoku("Samurai")
    new_Samurai.SetDiagonal()
    print(new_Samurai)
    new_Samurai.SetSudValues()
    print(new_Samurai)
    new_Samurai.SetPuzzle()
