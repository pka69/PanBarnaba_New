const dead_or_live = [
    [0,0],
    [0,0],
    [0,1],
    [1,1],
    [0,0],
    [0,0],
    [0,0],
    [0,0],
    [0,0],
]

var MANUAL = false; //user can chage cell stage manually
var INTERVAL = 125; //one step time
var STOP = false;
var timimg = NaN; // place for interval function

function stage_change_manually(item) {
        var x= Math.floor(item.dataset['x'])
        var y= Math.floor(item.dataset['y'])
        var cell = grid.cells[x * grid.cols + y]
    if (item.classList[1] === 'deadCell') {
        item.classList.remove('deadCell')
        item.classList.add('liveCell')
        cell.stage=1
    }
    else {
        item.classList.remove('liveCell')
        item.classList.add('deadCell')
        cell.stage=0
    }
}

class Cell {
    constructor(item,x,y) {
        this.item = item;
        this.x = x;
        this.y = y;
        this.neighbors =[];
        this.stage = 0;
        this.next_stage = 0;
        // this.item.addEventListener('mousedown', function() {mouseIsDown = true})
        // this.item.addEventListener('mouseup', function() {mouseIsDown = false})
    }
    coord() {
        return this.x + "-" +this.y
    }
    update_manual() {
        if (MANUAL) {
            this.item.addEventListener('mousedown', function mouseOver(event) {
                if (MANUAL) {
                    var button = event.currentTarget
                    if (event.buttons===1) {stage_change_manually(button)} 
                }
            })
            this.item.addEventListener('mouseover', function mouseOver(event) {
                if (MANUAL) {
                    var button = event.currentTarget
                    if (event.buttons===1) {stage_change_manually(button)} 
                }
            })
        }
    }
    add_neighbor(item) {
            this.neighbors.push(item)
    }
    del_neighbor(item) {
        for(i=0;i++; i<this.neighbors.length) {
            if (this.neighbors[i].coord() === item()) {
           this.neighbors = this.neighbors.slice(pos); 
            }
        }
    }
    init_stage(stage) {
        this.next_stage = stage
    }
    live_neighbors_count() {
        var i = 0;
        for (var neighbor of this.neighbors) {
            if (neighbor.stage == 1) {
                i ++
            }
        }
        return i
    }
    next_stage_count() {
        var i = this.live_neighbors_count()
        this.next_stage = dead_or_live[i][this.stage]
        // this.next_stage = ((dead_or_live[this.stage].includes(i))?1:0)
        // console.log(i, dead_or_live[this.stage], dead_or_live[this.stage].includes(i))
        // console.log('item ',this.x, this.y,
        //             'i:', i, dead_or_live[i],
        //             'stage, next:', this.stage, this.next_stage)
        return this.next_stage
    }
    next_stage_move() {
        if (!(this.stage == this.next_stage)) {
            // console.log('item ',this.x, this.y, 
            //         'stage, next:', this.stage, this.next_stage, " i'm change!")
            this.stage = this.next_stage;
            if (this.stage ===1) {
                this.item.classList.add('liveCell')
                this.item.classList.remove('deadCell')
            }
            else {
                this.item.classList.add('deadCell')
                this.item.classList.remove('liveCell')
            }
            return true;
        }
        return false;
    }
    get_stage(){
        console.log('item ',this.x, this.y, 
                    'stage, next:', this.stage, this.next_stage)
    }
}
class Grid {
    constructor(cells, rows, cols, x_around,y_around) {
        this.cells = cells;
        this.rows = rows;
        this.cols = cols;
        this.x_around = x_around;
        this.y_around = x_around;
        this.steps = 0;
        this.change = 0;
        for (var row=0;row<this.rows;row++) {
            for (var col=0;col<this.cols; col++) {
                for (var i=-1;i<2;i++ ){
                    for (var j=-1;j<2;j++ ) {
                        var x = row + i;
                        var y = col + j;
                        if (x<0 && x_around) {x = this.rows -1}
                        if (x>=this.rows && x_around) {x = 0}
                        if (y<0 && y_around) {y = this.cols -1}
                        if (y>=this.cols && y_around) {y = 0}
                        if (x>=0 && x<this.rows && y>=0 && y<this.cols){
                            if((x!=row ) || (y!=col)){
                                this.cells[row*this.cols+col].add_neighbor(this.cells[x*this.cols+y])
                            }
                        }
                    }
                }
            }
        }
    }
    next_stage_count() {
        for (var cell of this.cells) {
            cell.next_stage_count()
        }   
    }
    next_stage_move() {
        this.change = 0;
        for (var cell of this.cells) {
            if (cell.next_stage_move()) {
                this.change = 1;
            }
        }
        this.steps ++
    }
    get_stage(){
        for (var cell of this.cells) {
            cell.get_stage()
        }
    }
    show_change() {
        for (var cell of this.cells)  {
            if (cell.stage==1 || cell.next_stage==1 ){
                console.log('item:', row, col, 'lnc:', cell.live_neighbors_count(),'stage:', cell.stage, 'next_stage', cell.next_stage)
            }
        }
    }
    generator(how_many) {
        var no_items = Math.floor(how_many * this.cells.length)
        console.log('do wygenerowania:', no_items)
        for (var cell of this.cells)  {
            if (cell.stage==1) { no_items-- }
        }
        console.log('do wygenerowania 2:', no_items)
        var limit = this.cells.length
        var rnd_cell = Math.floor(Math.random() * (limit))
        var cell = this.cells[rnd_cell]
        while (no_items>0) {
            if (cell.stage===0) {
                cell.stage = 1;
                cell.item.classList.remove('deadCell')
                cell.item.classList.add('liveCell')
                no_items--
            }
            rnd_cell = Math.floor(Math.random() * (limit))
            cell = this.cells[rnd_cell]
        }
    }
    reset() {
        for (var cell of this.cells) {
            if (cell.stage===1) {
                cell.stage = 0;
                cell.item.classList.remove('liveCell')
                cell.item.classList.add('deadCell')
            }
        }
        this.steps = 0;
    }
    switch_x_around() {
        if (this.x_around) {
            for (var i=0;i++;i<this.colls) {
                this.cells[i].del_neighbor(this.cells[(this.rows-1)*this.cols+i])
                this.cells[(this.rows-1)*this.cols+i].del_neighbor(this.cells[i])
            }
            this.x_around = false;
        }
        else {
            for (var i=0;i++;i<this.colls) {
                this.cells[0][i].add_neighbor(this.cells[this.rows][i])
                 this.cells[this.rows][i].add_neighbor(this.cells[0][i])
            }
            this.x_around = true;
        }
    }
    switch_y_around() {
        if (this.y_around) {
             for (var i=0;i++;i<this.rows) {
                this.cells[i][0].del_neighbor(this.cells[this.rows][i])
            }
            this.y_around = false;
        }
        else {
            for (var i=0;i++;i<this.colls) {
                this.cells[0][i].add_neighbor[this.cells[this.rows][i]]
            }
            this.y_around = true;
        }
    }
}

let grid = ''
if (document.getElementsByName("gols").length) {
    var cells = []
    var rows = document.getElementsByName("rows")[0].value
    var cols = document.getElementsByName("cols")[0].value

    var item_cells_hidden = document.querySelectorAll(".cell_hidden")
    var item_cells = document.querySelectorAll(".cell")
    console.log(item_cells.length, item_cells_hidden.length )
    // var x1 = Math.round(rows/4);
    // var x2 = Math.round((3 * rows)/4);
    // var y1 = Math.round(cols/4);
    // var y2 = Math.round((3 * cols)/4);
    for (var i=0;i<(rows*1);i++){
        for (var j=0;j<(cols*1);j++) {
            cells.push(new Cell(item_cells[i * cols  + j],i,j))
            cells[i * cols  + j].update_manual()
            if (item_cells_hidden[i * cols + j].outerText === "1") {
                cells[i * cols  + j].init_stage(1)
            } 
            // if (i>=x1 && i<x2 && j>=y1 && j<y2) {
            //     if (item_cells_hidden[(i - x1) * Math.round(cols /2)  + Math.round(j-y1)].outerText === "1") {
            //         cells[i * cols  + j].init_stage(1)
            //     }
            // }
            cells[i * cols  + j].next_stage_move()
        }
    }
    const repeater = document.getElementsByName("repeater")[0]
    
    grid = new Grid(cells, rows, cols, repeater.dataset['repeater_x']=="True", repeater.dataset['repeater_y']=="True");
    timing = setInterval(
    function() {
        grid.next_stage_count();
        grid.next_stage_move();
        if (STOP) {
            clearInterval(timing);
        }
    }, INTERVAL)
} 
else {
    var cells = []
    MANUAL = true
    STOP = true
    var rows = document.getElementsByName("rows")[0].value
    var cols = document.getElementsByName("cols")[0].value
    var item_cells = document.querySelectorAll(".cell2")
    console.log(item_cells.length)
    for (var i=0;i<(rows*1);i++){
        for (var j=0;j<(cols*1);j++) {
            cells.push(new Cell(item_cells[i * cols  + j],i,j))
            cells[i * cols  + j].init_stage(0)
            cells[i * cols  + j].update_manual()
            cells[i * cols  + j].next_stage_move()
        }
    }
    grid = new Grid(cells, rows, cols, false, false);
    var live = document.getElementsByName("live")
    for (item of live) {
        item.addEventListener('click', function(event) {
            console.log(STOP, (STOP===false))
            console.log('click2')
            if (STOP===false) return;
            var button = event.currentTarget;
            var no = button.outerText * 1
            if (button.classList.contains('cell_selected')) {
                button.classList.remove('cell_selected');
                dead_or_live[no][1] = 0;
            }
            else {
                button.classList.add('cell_selected');
                dead_or_live[no][1] = 1;
            }
        })
    }
    var born = document.getElementsByName("born")
    for (item of born) {
        item.addEventListener('click', function(event) {
            if (!(STOP)) {return}
            var button = event.currentTarget;
            var no = button.outerText * 1
            if (button.classList.contains('cell_selected')) {
                button.classList.remove('cell_selected');
                dead_or_live[no][0] = 0;
            }
            else {
                button.classList.add('cell_selected');
                dead_or_live[no][0] = 1;
            }
        })
    }    
    var generator = document.getElementsByName("generator");
    for (item of generator) {
        item.addEventListener('click', function(event) {
            if (!(STOP)) {return}
            var button = event.currentTarget;
            button.classList.add('cell_selected');
            var no = parseFloat(button.outerText)/100
            grid.generator(no)
            button.classList.remove('cell_selected');
        })
    }
    var speed = document.getElementsByName("speed");
    for (item of speed) {
        item.addEventListener('click', function(event) {
            if (!(STOP)) {return}
            var button = event.currentTarget;
            INTERVAL = button.outerText * 1;
            console.log(INTERVAL)
            for (var item of button.parentElement.children) {
                if (item===button) {
                  item.classList.add('cell_selected')  
                }
                else {
                    item.classList.remove('cell_selected')
                }
            }
        })
    }  
    var oneStep = document.getElementsByName("oneStep")[0];
    oneStep.addEventListener('click', function() {
        if (!(STOP)) {return}
        grid.next_stage_count()
        grid.next_stage_move()
    })
    var reset = document.getElementsByName("reset")[0];
    reset.addEventListener('click', function() {
        if (! STOP) {return}
        grid.reset()
    })
    var start = document.getElementsByName("start")[0];
    start.addEventListener('click', function(event) {
        var button = event.currentTarget;
        if (!(STOP)) {
            STOP = true;
            button.classList.remove('btn-secondary')
            button.classList.add('btn-outline-secondary')
            button.innerText = 'Uruchom algorytm życia'
            // document.getElementsByName("noSteps")[0].classList.add('d-none')
            grid.steps = 0;
            clearInterval(timing);
            return
        }
        button.classList.remove('btn-outline-secondary')
        button.classList.add('btn-secondary')
        button.innerText = 'Zatrzymaj algorytm życia'
        document.getElementsByName("noSteps")[0].classList.remove('d-none')
        STOP = false;
        timing = setInterval(
            function() {
                grid.next_stage_count();
                grid.next_stage_move();
                document.getElementsByName("noSteps")[0].innerText = "krok nr: " + grid.steps
                if (grid.change==0) {
                    document.getElementsByName("start")[0].click()
                }
            }, INTERVAL)
    })
}