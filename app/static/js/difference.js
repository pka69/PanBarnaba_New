const diffs = document.getElementsByName("diff");
const level = parseInt(document.getElementById("level").innerText);
const blocksize = parseInt(document.getElementById("blocksize").innerText);
const msg = document.getElementById("msg")


function odmiany(number) {
    switch (number) {
        case 1: 
            return `${number} pomyłka`;
        case 2: 
            return `${number} pomyłki`;
        case 3: 
            return `${number} pomyłki`;    
        case 4: 
            return `${number} pomyłki`;
        default: 
            return `${number} pomyłek`;
    }
}


class diffPart {
    constructor(img_object){
        this.img = img_object;
        this.x = parseInt(img_object.dataset.x);
        this.y = parseInt(img_object.dataset.y);
        this.diff = parseInt(img_object.dataset.diff);
        this.selected = false;
        
    }
    clicked() {
        this.selected = true;
        this.img.firstElementChild.classList.remove("d-none")
        this.img.removeEventListener('click', clickReact )
        return this.diff;
    }

}
function clickReact(event) {
    const x = parseInt(event.target.dataset.x);
    const y = parseInt(event.target.dataset.y);
    diff = parseInt(event.target.dataset.diff);
    console.log(x, y, diff);
    findDiff.clicked(x, y, diff)

}
class differences {
    constructor(){
        this.diffs = []
        this.blocksize = blocksize
        this.mistakes = 0
        diffs.forEach((element)=>{
            this.diffs.push(new diffPart(element));
            element.addEventListener('click', clickReact, {once: true})
        })
        this.toFind = Math.max(...this.diffs.map((el) => el.diff))
        this.finded = this.toFind
    }
    message() {
        msg.innerText = `poszukaj ${this.finded} różnic ` + (this.mistakes?`(${odmiany(this.mistakes)})`:'.');
        console.log(`poszukaj ${this.finded} różnic ` + (this.mistakes?`(${odmiany(this.mistakes)})`:'.'))
    }
    finished() {
        let result = (this.toFind) / (this.toFind + this.mistakes) * 100.0
        result = Math.round(result * 100.0 ) / 100
        document.getElementById("result").innerText = result + "%"
        finish.innerText = 1 
        this.diffs.map((el) => el.img.removeEventListener('click', clickReact ))
    }
    clicked(x, y, diff) {

        if (diff) {
            this.diffs.filter((el) => el.diff == diff).forEach((el) =>el.clicked())
            this.finded --;
            this.message();
            if (this.finded == 0) {
                this.finished()
                return
            }
        } 
        else {
            this.diffs[x * this.blocksize + y].clicked()
            this.mistakes ++;
            this.message();
        }
    }
}

const findDiff = new differences()