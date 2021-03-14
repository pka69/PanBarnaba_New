
var MANUAL = true;
var STOP = true;
var FINISH = false;
var INTERVAL = 125;
var OnGoing = 0;
var START_POINT = false;
var END_POINT = false;
const ResetButton = document.getElementById('reset')
const resultMessage = document.getElementById('resultMessage')

const msg = document.getElementById('msg')

const AROUND = [
    [-1,0],
    [1,0],
    [0,-1],
    [0,1]
]

function resultMessageShow() {
    resultMessage.style.display = "block";
    // TopList.style.paddingRight = "17px";
    resultMessage.className="modal fade show"; 
  }

  function resultMessageHide() {
    resultMessage.style.display = "none";
    resultMessage.className="modal fade";
  }

if (document.getElementById('Close1')){
    document.getElementById('Close1').addEventListener('click', resultMessageHide)
    document.getElementById('Close2').addEventListener('click', resultMessageHide)
}

function stage_change_manually(item) {
    var x= Math.floor(item.dataset['x'])
    var y= Math.floor(item.dataset['y'])
    var value = Math.floor(item.dataset['value'])
    var cell = grid.get_cell(x,y)
    if (START_POINT) {
        console.log('make start')
        START_POINT = false
        document.body.style.cursor = "default"
        msg.innerText = 'Status: wycinaj korytarze/uzupelniaj mur'
        item.classList.remove('liveWall')
        item.classList.remove('deadWall')
        item.classList.add('startLab');
        cell.stage = -1
        if (grid.start != null) {
            grid.start.item.classList.remove('startLab');
            grid.start.item.classList.add('liveWall');
            grid.start.value = 1
        }
        grid.start = cell
        grid.roads[0] = [cell]
        return
    }
    if (END_POINT) {
        console.log('make end')
        END_POINT = false
        document.body.style.cursor = "default"
        msg.innerText = 'Status: wycinaj korytarze/uzupelniaj mur'
        item.classList.remove('liveWall')
        item.classList.remove('deadWall')
        item.classList.add('endLab');
        cell.stage = -2
        if (grid.end != null) {
            grid.end.item.classList.remove('endLab');
            grid.end.item.classList.add('liveWall');
            grid.end.value = 1
        }
        grid.end = cell
        return
    }
    if (item.classList.contains('liveWall')) {
        item.classList.remove('liveWall');
        item.classList.add('deadWall');
        item.dataset['value'] = "0"
        cell.stage = 0
        // console.log(cell.x, cell.y)
    }
    else {
        item.classList.add('liveWall');
        item.classList.remove('deadWall');
        item.dataset['value'] = "1"
        cell.stage = 1
        // console.log(cell.x, cell.y)
    }
}
function switch_off(item) {
    item.firstElementChild.classList.remove('roadLight')
    item.firstElementChild.classList.add('roadStep')
}
function switch_on(item) {
    item.firstElementChild.classList.remove('d-none')
    item.firstElementChild.classList.remove('roadStep')
    item.firstElementChild.classList.add('roadLight')
    if (OnGoing>0){OnGoing--}
}
function reset_road_item(item) {
    // switch_off(item);
    item.firstElementChild.classList.add('d-none')
    item.firstElementChild.classList.remove('roadLight')
    item.firstElementChild.classList.remove('roadStep')
    item.firstElementChild.innerText = '';
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }
  
class Cell {
    constructor(item,x,y) {
        this.item = item;
        this.x = x;
        this.y = y;
        this.neighbors =[];
        this.stage = item.dataset["value"] * 1;
    }
    coord() {
        return this.x + "-" +this.y
    }
    update_manual() {
        // if (this.y=49) {console.log("set event", this.x, this.y, this.item)}
        this.item.addEventListener('mouseover', function mouseOver(event) {
            if (MANUAL) {
                var button = event.currentTarget
                if (event.buttons===1) {stage_change_manually(button)} 
            }
        })
        this.item.addEventListener('mousedown', function mouseOver(event) {
            if (MANUAL) {
                var button = event.currentTarget
                if (event.buttons===1) {stage_change_manually(button)} 
            }
        })
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
        this.stage = stage;
    }
    set_stage(stage) {
        if (stage !== this.stage) {
            this.stage = stage;
            this.item.firstElementChild.innerText = stage;
            switch_on(this.item)
        }
        else {
            switch_off(this.item)
        }
    }

    next_stage_count() {
        var i = [];
        for (var neighbor of this.neighbors) {
            if (neighbor.stage == 0 || neighbor.stage == -2) {
                i.push(neighbor)
            }
        }
        return i
    }

    get_stage(){
        console.log('item ',this.x, this.y, 
                    'stage:', this.stage)
    }
}
class Grid {
    constructor(cells, rows, cols) {
        this.cells = cells;
        this.rows = rows;
        this.cols = cols;
        this.roads = []
        this.start = null;
        this.end = null;
        this.finish = false;
        this.posibility = true;
        for (var row=0;row<this.rows;row++) {
            for (var col=0;col<this.cols; col++) {
                if(this.cells[row*this.cols+col].stage==-1) {
                    this.start = this.cells[row*this.cols+col]
                    this.roads[0] = [this.cells[row*this.cols+col]]
                }
                if(this.cells[row*this.cols+col].stage==-2) {this.end = this.cells[row*this.cols+col]}
                for (var i of  AROUND ){
                    var x = row + i[0];
                    var y = col + i[1];
                    if (x>=0 && x<this.rows && y>=0 && y<this.cols){
                        if((x!=row ) || (y!=col)){
                            this.cells[row*this.cols+col].add_neighbor(this.cells[x*this.cols+y])
                        }
                    }
                }
            }
        }
    }
    update_manual() {
        for (var item of this.cells) {
            item.update_manual()
        }
    }
    next_stage_count() {
        var posibility = 0
        if (this.finish){return}
        var counter = 0;
        for (var road of this.roads) {
            counter ++;
            switch_off(road[road.length-1].item)
            var possibles_step = road[road.length-1].next_stage_count()
            if (possibles_step.length > 1) {
                var temp_road = [];
                for (var item of road) {
                    temp_road.push(item); 
                }    
                this.roads.push(temp_road);
            }
            if (possibles_step.length > 0){
                posibility ++
                road.push(possibles_step[0])
                road[road.length-1].set_stage(road.length)
                if (possibles_step[0] === this.end) {this.finish = counter}
            }
        }
        if (posibility == 0) {
            this.posibility = false;
        }
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

    show_win_road(clean = false){
        if (!this.finish) {
            return;
        }
        var counter = 0
        for (var item of this.roads[this.finish-1]) {
            switch_on(item.item);
            // sleep(125)
            counter++;
            // OnGoing++;
            // setTimeout(switch_on, 50*counter,item.item)
        }
        console.log(counter)
        console.log(OnGoing)
        // if (clean) {
        //     for (var item of this.roads[this.finish-1]) {
        //         setTimeout(this.reset, 50*(counter + 2))
        //     }
        // }
    }
    reset() {
        for (var road of this.roads) {
            for (var item of road) {
                reset_road_item(item.item)
                item.init_stage(0)
            }
        }
        this.finish = false;
        this.roads = [];
        if (this.start !== null) {
            this.roads[0] = [this.start]
            this.start.init_stage(-1)
        }
        if (this.end !== null){this.end.init_stage(-2)}
        for (var item in this.cells){
            if (cells.stage==0){reset(item.item)}
        }
        this.posibility = true;
    }

    get_cell(x, y) {
        return this.cells[x * this.cols + y]
    }
    ready_to_run() {
        console.log('ready_to_run chcek')
        if ((this.start != null) & (this.end != null)) {return true}
        console.log('not ready_to_run')
        return false
    }
}


var demo = document.getElementById("demo")
var grid = null

var cells = []
var rows = document.getElementsByName("rows")[0].value
var cols = document.getElementsByName("cols")[0].value
var item_cells = document.querySelectorAll(".cell3")
for (var i=0;i<(rows*1);i++){
    for (var j=0;j<(cols*1);j++) {
        cells.push(new Cell(item_cells[i * cols  + j],i,j))
        cells[i * cols  + j].update_manual()
    }
}
grid = new Grid(cells, rows, cols)

if (demo) {
    MANUAL = false;
    STOP = false;
    ResetButton.addEventListener('click', function() {
        STOP = false;
        grid.reset()
        ResetButton.classList.add('disabled')
        timing = setInterval(
            function() {
                if (STOP) {
                    clearInterval(timing);
                    ResetButton.classList.remove('disabled')
                    console.log('stop interval')
                    return
                }
                if (FINISH) {
                    FINISH = false;
                    STOP = true;
                    // grid.reset();
                    return;
                }
                if (!grid.finish){
                    grid.next_stage_count();
                }
                else {
                    grid.show_win_road(true);
                    FINISH = true;
                }
                
            }, INTERVAL)
    })
    timing = setInterval(
        function() {
            if (STOP) {
                clearInterval(timing);
                ResetButton.classList.remove('disabled')
                console.log('stop interval')
                return
            }
            if (FINISH) {
                FINISH = false;
                STOP = true;
                // grid.reset();
                return;
            }
            if (!grid.finish){
                grid.next_stage_count();
            }
            else {
                grid.show_win_road(true);
                FINISH = true;
            }
            
        }, INTERVAL)
}
else {
    MANUAL = true
    STOP = true
    // grid.update_manual()
    var StartPoint = document.getElementById("start")
    StartPoint.addEventListener("click", function() {
        START_POINT = true;
        END_POINT = false;
        document.body.style.cursor = "move"
        msg.innerText = "Status: Wskaż początek labiryntu"
    })
    var EndPoint = document.getElementById("end")
    EndPoint.addEventListener("click", function() {
        END_POINT = true;
        START_POINT = false;
        document.body.style.cursor = "move"
        msg.innerText = "Status: Wskaż punkt docelowy labiryntu"
    })
    document.getElementById("oneStep").addEventListener('click', function() {
        
        if (grid.ready_to_run()) {
            grid.next_stage_count()
        }
    })
    document.getElementById('reset').addEventListener('click',function() {
        grid.reset()
    })
    document.getElementById('startRoad').addEventListener('click', function(event) {
        console.log('road start')
        ResetButton.classList.add('disabled');
        document.getElementById("oneStep").classList.add('disabled');
        var button = event.currentTarget;
        if(!(STOP)) {
            STOP = true;
            button.classList.remove('btn-secondary')
            button.classList.add('btn-outline-secondary')
            button.innerText = 'Uruchom szukanie drogi życia'
            clearInterval(timing);
            return
        }
        MANUAL = false;
        STOP = false;
        FINISH = false;
        button.classList.remove('btn-outline-secondary')
        button.classList.add('btn-secondary')
        button.innerText = 'Zatrzymaj szukanie drogi'
        timing = setInterval(
            function() {
                console.log('interval step')
                if (grid.posibility == 0) {
                    console.log("grid possibility;",grid.posibility)
                    STOP=true;
                    resultMessageShow()
                    // grid.reset()
                }
                if (STOP) {
                    clearInterval(timing);
                    MANUAL = true;
                    ResetButton.classList.remove('disabled')
                    document.getElementById("oneStep").classList.remove('disabled')
                    button.classList.remove('btn-secondary')
                    button.classList.add('btn-outline-secondary')
                    button.innerText = 'Uruchom szukanie drogi życia'
                    console.log('stop interval')
                    return
                }
                if (FINISH) {
                    FINISH = false;
                    STOP = true;
                    // grid.reset();
                    return;
                }
                if (!grid.finish){
                    grid.next_stage_count();
                }
                else {
                    grid.show_win_road(true);
                    FINISH = true;
                }
            }, INTERVAL)
    })
}