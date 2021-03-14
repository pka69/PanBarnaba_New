import hashlib

from django.db import IntegrityError

from tools.sudoku_object import Sudoku as S
from sudoku.models import Sudoku, Cell, Block


def createSudoku():

    def blocks_cells_create():
        for item in sudoku.items:
            try:
                cell = Cell.objects.create(
                    x=item.x,
                    y=item.y,
                    fix=item.fix,
                    value=0 if item.hidden else item.fix_value,
                    hidden=item.hidden,
                    border=item.decor,
                    sudoku=sudoku_model
                )
            except Exception as ex:
                print("nie można dodać sudoku cell  {}.\n{}".format(item.coord, ex))
                input('naciśnij enter, aby pójśc dalej')
                continue
            sudoku_model.cells.add(cell)
            for block in item.blocks:
                s_block = blocks.get(block.name, '')
                if not s_block:
                    try:
                        s_block = Block.objects.create(sudoku=sudoku_model, name=block.name)
                        blocks[block.name] = s_block
                    except Exception as ex:
                        print("nie można dodać sudoku block {}.\n{}".format(block.GetName, ex))
                        input('naciśnij enter, aby pójśc dalej')
                        continue
                cell.blocks.add(s_block)

    steps = [
        [4, 10],
        [9, 5],
        ['Samurai', 2]
    ]
    Sudoku.objects.filter(level='Samurai').delete()
    for s_type, s_count in steps:
        blocks = {}
        i = 0
        while i < s_count:
            sudoku = S(s_type)
            sudoku.SetSudValues()
            sudoku.SetPuzzle()
            try:
                sudoku_model = Sudoku.objects.create(
                    slug=hashlib.md5(sudoku.Slug().encode()).hexdigest(),
                    level=s_type,
                    size=sudoku.type
                )
            except Exception as ex:
                print("nie można dodać sudoku.\ntyp {}\nslug {}\n{}".format(s_type, sudoku.Slug(), ex))
                input('naciśnij enter, aby pójśc dalej')
                continue
            else:
                print("dodano sudoku {}".format(sudoku.Slug))
            i += 1
            blocks_cells_create()
