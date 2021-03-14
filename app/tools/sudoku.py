from itertools import combinations
from math import sqrt
from random import choice, shuffle

from .block import Item, Block


class SudItem(Item):
    '''
    Item class dedicated to sudoku.Item
    Additional decor value
    '''
    def __init__(self, x=0, y=0, last_move=None, value='', hidden=False, decor=''):
        super().__init__(x=0, y=0, last_move=None, value='', hidden=False)
        self.__decor = decor

    @property
    def decor(self):
        return self.__decor

    def SetDecor(self, decor):
        self.__decor = decor

    def SetRandomValue(self):
        ava = self.GetRange()
        if not ava:
            return False
        return self.SetValue(choice(list(ava)))

    def GetRangeIf(self):
        if not self.value:
            return self.GetRange()
        s = self.value
        self.DelValue()
        r = self.GetRange()
        self.SetValue(s)
        return r

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

    @ property
    def size(self):
        return len(self.__item_list)

    @ property
    def lastitem(self):
        if not len(self.__item_list):
            return list()
        return self.__item_list[0], self.__value_list[0][0], self.__value_list[0][1]

    def DelHistoryAll(self):
        self.__item_list.clear()
        self.__value_list.clear()


class SudBlock(Block):
    '''
    sudoku block (2 x 2, 3 x 3)
    '''
    def __init__(self, name, size=9, values='123456789', decor=True):
        super().__init__(name, size=9, values='123456789')
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

    def AddItem(self, item):
        if super().AddItem(item):
            if self.__decor:
                item.SetDecor(self.__decor[len(self.items) - 1])
            return True
        return False

    def SetItems(self):
        if not len(self.values):
            return True
        if len([item for item in self.items if len(item.GetRange()) == self.size]) == self.size:
            for item in self.items:
                item.SetValue(choice(list(item.GetRange())))
            return True
        counter = 1
        while [item for item in self.items if item.EmptyItem]:
            if not self.GetOnlyOne():
                item = choice(
                    [item for item in self.items if not item.value])
                if item.NoMove:
                    self.ClearAll()
                    counter += 1
                    continue
                if not item.SetRandomValue():
                    self.ClearAll()
            else:
                item, val = self.GetOnlyOne()
                if not item.SetValue(val):
                    self.ClearAll()
                    counter += 1
            if counter == 20:
                return False
        return True

    def GetNoMove(self):
        pos = []
        pos.extend([(item, item.GetRange(True))
                    for item in self.items if item.NoMove()])
        return pos[0] if len(pos) else pos

    def GetOnlyOne(self):
        pos = []
        pos.extend([(item, item.GetRange(True))
                    for item in self.items if len(item.GetRange()) == 1])
        return pos[0] if len(pos) else pos

    def ClearAll(self):
        for item in self.items:
            if item.value:
                item.DelValue()

    def GetOut(self, output_list):
        for item in self.items:
            item.GetOut(output_list)

    def GetItemValues(self):
        ava = set()
        for item in self.items:
            ava |= set(item.value)
        return ava

    def GetItemWithValue(self, value):
        for item in self.items:
            if item.value == value:
                return item
        return None


class Sudoku:
    '''
    main Sudoku object includes blocks (2x2 or 3x3) and cells
    '''
    def __init__(self, type=9, sub_samurai=None, parent=None, last_move=None):
        self.items = []
        self.blocks = []
        self.type = type
        self.sub = []
        if parent:
            self.parent = parent
            self.last_move = last_move
        else:
            self.last_move = LastMove()

        def blocksindex(name, _type, _hidden):
            ind = list(filter(lambda bl: bl.name == name, self.blocks))
            if ind:
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
                        if not len(list(filter(lambda block: block.name == bl.name, self.blocks))):
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
                    block.AddItem(item)
                    row.AddItem(item)
                    col.AddItem(item)
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

    def Slug(self):
        return ''.join([item.value for item in self.items])

    def SetDiagonal(self, reverse=False):
        if any(item.fix for item in self.items if not item.hidden):
            return
        if self.sub:
            i = 0
            for s in self.sub:
                i += 1
                s.SetDiagonal(not (i % 2))
            return
        temp_block = [block for block in self.blocks if block.name.count(
            '_') == 2 and block.values]
        for block in temp_block:
            sek = block.name.split('_')
            if reverse:
                sek[1] = str(6 - int(sek[1]))
            if (int(sek[1]) % 4) == (int(sek[2]) % 4):
                i = 0
                while [item for item in block.items if item.EmptyItem]:
                    block.SetItems()
                    while [item for item in self.items if item.EmptyItem and item.NoMove]:
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
            updateEmptyItems()
            while [item for item in empty_items if item.NoMove]:
                last_item = self.last_move.lastitem
                while last_item[2] <= int(sqrt(self.type)):
                    item = last_item[0]
                    if item.DelValue():
                        empty_items.append(item)
                    last_item = self.last_move.lastitem
                if self.last_move.size < 2:
                    return
                for _ in range(2):
                    last_item = self.last_move.lastitem
                    item = last_item[0]
                    if item.DelValue():
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
                if item.SetValue(str(only_one_items[0][1])):
                    empty_items.pop(empty_items.index(item))
                    updateOnlyOne()
                else:
                    break_flag = True
            if len(empty_items) and not break_flag:
                item = choice(empty_items)
                OK = item.SetRandomValue()
                if OK:
                    empty_items.pop(empty_items.index(item))
                else:
                    break_flag = True
                    # self.last_move.DelLast()
            if break_flag:
                clearIfNoMove()
                break_flag = False
        self.last_move.DelHistoryAll()
        return True

    def CheckCritical4(self):
        '''
        critical situation is when we have the same values in oposit possitions like this:
            x, 1, x, x, x, 3, x, x, x
            x, 3, x, x, x, 1, x, x, x
        one of this values has to be fix
        '''
        rows = []
        cols = []
        blocks = []
        items = ['', '', '', '']
        for block in self.blocks:
            if not block.name.find('row') == -1:
                rows.append(block)
            if not block.name.find('col') == -1:
                cols.append(block)
            if not block.name.find('block') == -1:
                blocks.append(block)
        values = blocks[0].GetRange
        for id, row in enumerate(rows, 1):
            for i_1, i_2 in combinations(values, 2):
                items[0] = row.GetItemWithValue(i_1)
                items[1] = row.GetItemWithValue(i_2)
                if not (items[1] in items[0].blocks[0].items):
                    continue
                for row2 in rows[id:]:
                    items[2] = row2.GetItemWithValue(i_1)
                    items[3] = row2.GetItemWithValue(i_2)
                    if (items[0].y == items[3].y) and (items[1].y == items[2].y):
                        if any([item.fix for item in items]):
                            break
                        item = choice(items)
                        item.setcopy
        for id, col in enumerate(cols, 1):
            for i_1, i_2 in combinations(values, 2):
                items[0] = col.GetItemWithValue(i_1)
                items[1] = col.GetItemWithValue(i_2)
                if not (items[1] in items[0].blocks[0].items):
                    continue
                for col2 in cols[id:]:
                    items[2] = col2.GetItemWithValue(i_1)
                    items[3] = col2.GetItemWithValue(i_2)
                    if (items[0].x == items[3].x) and (items[1].x == items[2].x):
                        if any([item.fix for item in items]):
                            break
                        item = choice(items)
                        item.setcopy

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
            block for block in self.blocks if block.name.count('_') == 2]
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
                        [item.decopy() for item in temp_item_list]
                        print(self)
                        return
                    for bl in range(step):
                        if (step) >= block_no:
                            if bl % block_no == 0:
                                shuffle(temp_block)
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
            temp_item_list = list(
                item for item in self.items if item.EmptyItem)
            i = len(temp_item_list)
            return i
