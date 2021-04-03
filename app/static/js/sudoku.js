const cells = document.querySelectorAll('.cell>p')
const numbers = document.querySelectorAll('.cell_n')
const key_numbers = []

for (i=1; i<numbers.length; i++) {
    key_numbers.push(String(i))
}
key_numbers.push('')

size = parseInt(document.querySelector('#size').innerText)
level = parseInt(document.querySelector('#level').innerText)

function Create2DArray(rows) {
  var arr = [];

  for (var i=0;i<rows;i++) {
     arr[i] = [];
  }

  return arr;
}

class Block {
    constructor(name) {
        this.name = name;
        this.cells = []
        this.values = []
        this.conflict = ''
    }
    addCell(cell){
        if (cell in this.cells) {
        }
        else {
            this.cells.push(cell)
            if (cell.cell.innerText.trim()!==''){
                this.values.push(parseInt(cell.cell.innerText))
            }
        }
    }
    removeValue(value){
        const i = this.values.indexOf(+value)
        // console.log('name:', this.name, 'value:', value, 'i:', i, 'this.values:', this.values)
        this.values.splice(i,1)
        // console.log('value:', value, 'i:', i, 'this.values:', this.values)
        if (this.conflict && this.conflict===value){
            // console.log('removed value = conflict value')
            if (this.values.filter(x => x===value).length === 1){
                // console.log('done')
                this.conflict = ''
            }
        }
        this.conflictMark()
    }
    addValue(value) {
        const i = this.values.indexOf(+value)
        // console.log("block.addValue", this.values, this.name, value, i)
        this.values.push(value)
        if (i!==-1){
            // console.log('conflict!!!', value)
           this.conflict = value 
        }
        this.conflictMark()
    }
    conflictMark() {
        for (var item of this.cells) {
            item.cell.parentElement.classList.remove('s_conflict');
            if (this.conflict === ''){
            }
            else if (this.conflict === item.cell.innerText) {
                item.cell.parentElement.classList.add('s_conflict');
            }
        }
    }
}

class SudokuCell {
    constructor(cell, blocks) {
        this.cell = cell;
        this.x = Number(cell.dataset.x);
        this.y = Number(cell.dataset.y);
        this.value = cell.dataset.value;
        this.blocks  = [];
        if (cell.dataset.fix =="True"){
            this.fix = true;
        }
        else {
            this.fix = false;
        }
        if (cell.dataset.hidden =="True"){
            this.hidden = true;
        }
        else {
            this.hidden = false;
        }
        var block_names = cell.dataset.blocks.split(',')
            block_names.splice(-1)
        for (var block of blocks) {
            if (block_names.includes(block.name)) {
                this.blocks.push(block)
                block.addCell(this)
            }
        }
    }
    compare(){
        if (this.cell.innerText === this.value){
            return true;
        }
        else {
            return false;
        }
    }
    valueChange(value){
        if (this.cell.innerText!==''){
            // console.log('usuwam starą wartość:',this.cell.innerText)
            for (var block of this.blocks) {
                block.removeValue(this.cell.innerText)
            }
            
        }
        this.cell.innerText = value;
        // console.log('podstawiam nową wartość:',this.cell.innerText)
        if (value!==''){
            // console.log('sprawdzanie konfliktu')
            for (var block of this.blocks) {
                block.addValue(value)
            }  
        }
        
    }
}

class Sudoku {
    constructor(){
        this.blocks = []
        this.cells = Create2DArray(size)
        this.active_cells = []
        this.active = NaN;
        var exist = [];
        self = this;
        for (var cell of cells) {
            var block_names = cell.dataset.blocks.split(',')
            block_names.splice(-1)
            for (var block of block_names) {
                if (exist.includes(block)) {
                }
                else {
                    this.blocks.push(new Block(block));
                    exist.push(block);
                }
            }
            this.cells[cell.dataset.x][cell.dataset.y] = new SudokuCell(cell, this.blocks)
            if (!(this.cells[cell.dataset.x][cell.dataset.y].hidden)) {
                if (!(this.cells[cell.dataset.x][cell.dataset.y].fix)) {
                    this.active_cells.push(this.cells[cell.dataset.x][cell.dataset.y])
                    const x = Number(cell.dataset.x)
                    const y = Number(cell.dataset.y)
                    this.cells[x][y].cell.parentElement.addEventListener('click', function cellClick() {
                        if (finish.innerText === "1") {
                            this.removeEventListener('click',cellClick);
                            return
                        }
                        onClick(x, y);
                    })
                }
            }
        }
        this.active = this.active_cells[0];
        this.active.cell.parentElement.classList.add('cell_active')
    }
    onClick(x,y) {
        const click = this.cells[x][y];
        this.active.cell.parentElement.classList.remove('cell_active')
        this.active = click;
        this.active.cell.parentElement.classList.add('cell_active')
    }
    key(direction){
        const move_options = [
            [0,-1],
            [1, 0],
            [0,1],
            [-1,0],
        ]
        const delta_x = move_options[direction][0]
        const delta_y = move_options[direction][1]
        var x = this.active.x + delta_x
        var y = this.active.y + delta_y
        while (true) {
            if (x>=0 && x< size){
                if (y>=0 && y< size) {
                    if (! (this.cells[x][y].hidden )) {
                        if (! (this.cells[x][y].fix)) {
                            this.onClick(x,y)
                            return
                        }
                    } 
                }
                else {
                    this.moveNext()
                    return
                }
            }
            else {
                this.moveNext()
                return
            }
            x = x + delta_x
            y = y + delta_y
        }
    }
    moveNext() {
        const pos = this.active_cells.indexOf(this.active)
        // if (pos == 0){
        //     onClick(this.active_cells[this.active_cells.length-1].x, this.active_cells[this.active_cells.length-1].y)
        // } else 
        if (pos == (this.active_cells.length - 1)){
            onClick(this.active_cells[0].x, this.active_cells[0].y)
        }
        else {
            onClick(this.active_cells[pos +1].x, this.active_cells[pos +1].y)
        }        
    }
    number(value){
        // console.log('number:', value)
        this.active.valueChange(value);
        // this.moveNext();
        this.isDone();
    }
    isDone() {
        function checkCompare(item) {
            var out = true;
            item.forEach(x => {
                if (x.compare()===false){
                    out = false
                    return out;
                }
            })
            return out;
        }
        const result = this.cells.every(checkCompare)
        if (result) {
            finish.innerText = 1     
            this.active.cell.parentElement.classList.remove('cell_active')    
        }
        return result
    }

}

const sudoku = new Sudoku()

function onClick( x, y) {
        sudoku.onClick(x, y)
    } 
function onNumber(x) {
    sudoku.number(x)
}
for (item of numbers) {
    const x = Number(item.innerText)
    item.addEventListener('click', function pressNumber() {
        if (finish.innerText === "1") {
            this.removeEventListener('click',pressNumber);
            return
        }
        if (x == 0) {
            sudoku.number('')    
        }
        else {
            sudoku.number(x)
        }
    })
}

function checkKey(event) {
    if (finish.innerText === "1") {
            this.removeEventListener('click',checkKey);
            return
        }

    const key = event.key; // "ArrowRight", "ArrowLeft", "ArrowUp", or "ArrowDown" 
    const key_arrows = [ "ArrowLeft", "ArrowDown", "ArrowRight",   "ArrowUp",]
    
    if (key_arrows.includes(key)) {
        event.preventDefault();
        sudoku.key(key_arrows.indexOf(key))
    }
    if (key_numbers.includes(key)) {
        event.preventDefault();
        sudoku.number(key)
    }
     if (key==' ' || key=="Delete" ) {
        event.preventDefault();
        sudoku.number('')
    }
    if (key=='Tab') {   
        event.preventDefault();
        sudoku.moveNext();
    }
     
}

document.addEventListener('keydown', checkKey )