var questions = document.querySelectorAll(".question")

var answers = document.querySelectorAll(".answer")




class Answer {
    constructor(item) {
        this.item = item;
        if(item.dataset['correct'] ==='True'){
            this.correct = true;
        } else {
            this.correct = false;
        }
    }
    is_correct() {
        if ((this.correct === this.item.checked) & this.correct) {
            return true;
        }
        return false;
    }
    result(multi) {
        if (this.is_correct()) {
            return 1;
        }
        if (multi) {
            if (this.item.checked) {
                return -1;
            } 
        }
        return 0;
    }
    color() {
        if (this.correct) {
            // this.item.nextElementSibling.classList.add('answer-correct')
            this.item.parentElement.classList.add('answer-correct')
            // this.item.nextElementSibling.innerText = this.item.nextElementSibling.outerText + ' - (ok)'
            return "ok"
        }
        if (this.item.checked) {
            // this.item.nextElementSibling.classList.add('answer-wrong')
            this.item.parentElement.classList.add('answer-wrong')
            // this.item.nextElementSibling.innerText = this.item.nextElementSibling.outerText + ' - (x)'
            return "x"
        }

    }
    block() {
        this.item.disabled = true;
        this.item.nextElementSibling.disabled = true;
        return "block"
    }
}

class Question {
    constructor(question) {
        this.question = question;
        this.id = question.dataset['id'];
        this.answers = [];
        this.expected = 0;
        for (var item of answers) {
            if (item.firstElementChild.dataset['question'] === this.id) {
                const answer = new Answer(item.firstElementChild);
                this.answers.push(answer);
                if(answer.correct) {this.expected ++ ;}
            }
        }
    }
    set_visible() {
            this.question.parentElement.classList.remove('d-none');
        }
    result() {
        var temp_result = 0;
        for (var item of this.answers) {
            temp_result += item.result(this.expected > 1);
        }
        temp_result = temp_result * 1.0 / this.expected
        if (temp_result < 0) {
            temp_result = 0
        }
        return temp_result;
    }
    block() {
        // this.question.parentElement.disabled = true;
        for (var item of this.answers){
            item.block()
        }
    }
    color() {
        // this.question.parentElement.disabled = true;
        for (var item of this.answers){
            item.color()
        }
    }
}

class Quiz {
    constructor() {
        this.actual = 0;
        this.questions = []
        for (var item of questions) {
            this.questions.push(new Question(item));
        }
        this.size = this.questions.length;
    }
    show_next() {
        this.questions[this.actual].block()
        this.actual ++
        if (this.actual === this.size ) {
            return false;
        }
        this.questions[this.actual].set_visible()
        return true;
    }
    result() {
        var temp_result = 0;
        for (var item of this.questions) {
            temp_result += item.result()
        }
        return temp_result * 100.0 / this.actual
    }
    color() {
        for (var item of this.questions){
            item.color()
        }
    }
}
function next_action() {
    if (quiz.show_next()) {
        end_site.scrollIntoView();
        } 
    else {
        finish.innerText = 1 
        quiz_result = quiz.result()
        document.getElementById("result").innerText = quiz_result + "%"
        next_button.classList.add('d-none');
        document.getElementsByName("next_game")[0].classList.remove('d-none');
        quiz.color();
    }
}
var quiz_result = 0
var quiz = new Quiz();
var next_button = document.getElementsByName("next_button")[0]
var end_site = document.getElementById("end_site")
next_button.addEventListener("click", function(event) {
    event.preventDefault();
    next_action()
})