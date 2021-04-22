const memos = document.getElementsByName("memos");
const level = parseInt(document.getElementById("level").innerText);

class memoPart {
    constructor(img_object){
        this.img = img_object;
        this.picture = img_object.dataset.picture;
        this.x = parseInt(img_object.dataset.x);
        this.y = parseInt(img_object.dataset.y);
        this.tempPicture = img_object.src;
        this.visible = false;
    }
    show() {
        console.log("show")
        this.selected = true;
        this.img.parentElement.classList.add("PB_image_memo_showcard");
        this.img.src = this.picture;
        return this.diff;
    }
    hide() {
        console.log("hide")
        this.selected = false;
        this.img.parentElement.classList.remove("PB_image_memo_showcard");
        this.img.src = this.tempPicture;
        return this.diff;
    }
    block() {
        this.img.removeEventListener('click', clickReact )
        this.visible = true;
    }
}

function clickReact(event) {
    const picture = event.target.dataset.picture;
    const x = parseInt(event.target.dataset.x);
    const y = parseInt(event.target.dataset.y);
    console.log(x, y, picture);
    memoMatcher.clicked(x, y, picture)

}

class memoSet {
    constructor(){
        this.memos = []
        this.blocksize = level
        this.selected = NaN
        memos.forEach((element)=>{
            this.memos.push(new memoPart(element));
            element.addEventListener('click', clickReact)
        })
        this.toFind = level * level
        this.finded = 0
    }
    finished() {
        finish.innerText = 1 
        this.memos.map((el) => el.img.removeEventListener('click', clickReact ))
    }
    clicked(x, y, picture) {
        console.log('start')
        this.memos[x * this.blocksize + y].show()
        const thisObject = this.memos[x * this.blocksize + y]
        const thisSelected = this.selected
        if (this.selected) {
            console.log('check')
            this.selected = NaN
            console.log(picture, thisSelected.picture, picture == thisSelected.picture)
            if (picture == thisSelected.picture) {
                // console.log('block',thisObject, thisSelected);
                thisObject.block();
                thisSelected.block();
                this.finded ++
                this.finded ++
                // this.selected = NaN
                console.log(this.toFind, this.finded)
                if (this.memos.filter(el => el.visible ==true).length == (level * level)) {this.finished()}
            }
            else {
                // this.selected = NaN
                setTimeout(() => { 
                    thisObject.hide();
                    thisSelected.hide();
                }, 1000);
                return
            }
            this.finded --;
            if (this.finded == 0) {
                this.finished()
                return
            }
        } 
        else {
            console.log('show')
            this.selected = this.memos[x * this.blocksize + y]
        }
    }
}

const memoMatcher = new memoSet()