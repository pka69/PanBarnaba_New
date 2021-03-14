const puzzle_parts = document.getElementsByName("ppart");
const level = parseInt(document.getElementById("level").outerText);
// const finish = document.getElementById('finish');


function deconstructPartDetail(part) {
    var src = part.getAttribute("src");
    var actual = part.dataset.actual;
    var origin = part.dataset.fix;
    // console.log(src, actual, fix);
    var path = "";
    fix = origin.split('.')[0];
    // console.log(fix)
    fix = fix.split('_');
    // console.log(fix)
    x = parseInt(fix[2]);   
    y = parseInt(fix[3]);
    // console.log("src-origin",src, actual)
    if (actual) {
        path = src.replace(actual,"");
    }
    // console.log("deconstruction:", path, x, y)
    return [path, x, y];
}

function Create2DArray(rows) {
  var arr = [];

  for (var i=0;i<rows;i++) {
     arr[i] = [];
  }

  return arr;
}


class PuzzlePart {
    constructor(img_object) {
        this.img = img_object;
        this.fix = img_object.dataset.fix;
        this.actual = img_object.dataset.actual;
        this.neighbors = []
        // console.log('dodano part:', this.fix, this.actual)
    }
    compare() {
        if (this.actual === '') {
            return true;
        }
        if (this.fix === this.actual){
            return true;
        }
        return false;
    }
    isEmpty() {
        if (this.actual === '') {
            return true;
        }
        return false;
    }
    changeActual(new_actual, path){
        this.actual = new_actual; 
        if (new_actual ==='') {
            this.img.setAttribute("src","")
            this.img.classList.add("d-none")
            return;
        }
        this.img.setAttribute("src",path + new_actual)
        this.img.classList.remove("d-none")
    }

}

class Puzzle {
    constructor() {
        this.parts = Create2DArray(level);
        this.path = '';
        this.empty = null;
        
        for (var part of puzzle_parts) {
            const result = deconstructPartDetail(part);
            const npath = result[0];
            const x = result[1];
            const y = result[2];
            // console.log("dodanawanie obiektu:", npath, x, y)
            if (this.path === ''){
                this.path = npath
            }
            this.parts[x][y] = new PuzzlePart(part)
            part.addEventListener('click', function mouseClick() {
                if (finish.innerText === "1") {
                    this.removeEventListener('click',mouseClick);
                    return
                }
                onClick( x, y);
            })
            // console.log('dodano element ', x, y, ":", this.parts[x][y])
            if (this.parts[x][y].isEmpty()) {
                this.empty = this.parts[x][y]
            }
        }
        for (var row=0;row<level;row++) {
            for (var col=0;col<level;col++) {
                var x = row - 1;
                if (x >=0 && x<level) {
                    this.parts[row][col].neighbors[0] = this.parts[x][col] 
                }
                else {
                    this.parts[row][col].neighbors[0] = null}
                var y = col + 1
                if (y >=0 && y<level) {
                    this.parts[row][col].neighbors[1] = this.parts[row][y] 
                }
                else {
                    this.parts[row][col].neighbors[1] = null}
                var x = row + 1;
                if (x >=0 && x<level) {
                    this.parts[row][col].neighbors[2] = this.parts[x][col] 
                }
                else {
                    this.parts[row][col].neighbors[2] = null}
                var y = col - 1
                if (y >=0 && y<level) {
                    this.parts[row][col].neighbors[3] = this.parts[row][y] 
                }
                else {
                    this.parts[row][col].neighbors[3] = null}
            }
        }   
    }
    onClick(x,y) {
        const click = this.parts[x][y];
        var action = false;
        click.neighbors.forEach(x => {
            if (x === this.empty) {
                action = true;
            }
        })
        if (action) {
            const temp = click.actual;
            click.changeActual('', this.path);
            this.empty.changeActual(temp, this.path);
            this.empty = click;
            this.isDone();
        }
    }
    key(direction){
        const move = this.empty.neighbors[direction]
        if (move === null) {
            return;
        }
        const temp = move.actual;
        move.changeActual('', this.path);
        this.empty.changeActual(temp, this.path);
        this.empty = move;
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
        const result = this.parts.every(checkCompare)
        if (result) {
            finish.innerText = 1          
        }
        return result
    }
}

const puzzle = new Puzzle()

function onClick( x, y) {
        puzzle.onClick(x, y)
    } 

document.addEventListener('keydown', function keyPress(event) {
    if (finish.innerText === "1") {
        this.removeEventListener('click',keyPress);
        return
    }
    const key = event.key; // "ArrowRight", "ArrowLeft", "ArrowUp", or "ArrowDown"
    const arrows = [ "ArrowLeft", "ArrowDown", "ArrowRight",   "ArrowUp",]
    if (arrows.includes(key)) {
        puzzle.key(arrows.indexOf(key))
    }
});
