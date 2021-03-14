document.querySelector("#main_content").focus();
var posts = document.querySelectorAll("[name='post']");
console.log('no of posts: ', posts.length);
var positives = document.querySelectorAll("[name='positives']");
console.log('no of positives flag: ', positives.length);
var negatives = document.querySelectorAll("[name='negatives']");
console.log('no of negatives flag: ', negatives.length);
var comments = document.querySelectorAll("[name='comments']");
console.log('no of comments counter: ', comments.length);
var add_comment = document.querySelectorAll("[name='add_comment']");
console.log('no of add_comment button: ', add_comment.length);
var comment_input = document.querySelectorAll("[name='comment_input']");
console.log('no of comment_input: ', comment_input.length);
var comment = document.querySelectorAll("[name='comment']");
console.log('no of comment: ', comment.length);
var subgroup = document.querySelector("[name='subgroup']")
console.log('subgroup:', subgroup)

function show_comment_input(id) {
    posts_list[id].comment_input.classList.remove('d-none');
    posts_list[id].comment_input.querySelector("[name='content']").focus();
}

function add_reactions(id, reaction) {
    temp_url = url.replace('forum','forum-react/'+reaction) + id
    fetch(temp_url)
        .then(response=> response.json())
            .then(data => {
                console.log(data)
                if (data["status"] == "success") {
                    var span = posts_list[id][reaction].querySelector("span")
                    span.innerText = (span.outerText * 1 + 1)
                }
                else if (data["status"] == "change") {
                    var positives = posts_list[id]['positives'].querySelector("span")
                    var negatives = posts_list[id]['negatives'].querySelector("span")
                    if (reaction=='negatives') {
                        positives.innerText = (positives.outerText * 1 - 1)
                        negatives.innerText = (negatives.outerText * 1 + 1)
                    } 
                    else {
                        positives.innerText = (positives.outerText * 1 + 1)
                        negatives.innerText = (negatives.outerText * 1 - 1)
                    }
                }
            })
            .catch(error => console.log(error));
}

function show_comments(id) {
    console.log
    for (var item of posts_list[id].comment) {
        item.classList.remove('d-none')
    }
}

class Post {
    constructor(id) {
        this.post = posts[id];
        this.id = this.post.dataset['id'];
        this.positives = positives[id];
        this.negatives = negatives[id];
        this.comments = comments[id];
        this.add_comment = add_comment[id];
        this.comment_input = comment_input[id];
        this.comment = []
        for (var item of comment) {
            if (item.dataset['post_id'] === this.id) {
                this.comment.push(item)
            }
        }

        this.add_comment.addEventListener('click', function(event) {
            var targetElement = event.target || event.srcElement;
            console.log(targetElement);
            var id = targetElement.dataset['post_id'];
            console.log(id);
            show_comment_input(id);
        })
        this.comments.addEventListener('click', function(event) {
            var targetElement = event.target || event.srcElement;
            console.log(targetElement);
            var id = targetElement.dataset['post_id'];
            show_comments(id)
        })
        this.positives.addEventListener('click', function(event) {
            var targetElement = event.target || event.srcElement;
            console.log(targetElement);
            var id = targetElement.dataset['post_id'];
            add_reactions(id, 'positives')
        })
        this.negatives.addEventListener('click', function(event) {
            var targetElement = event.target || event.srcElement;
            console.log(targetElement);
            var id = targetElement.dataset['post_id'];
            add_reactions(id, 'negatives')
        })
    }
}
posts_list = {}
console.log('start build posts_list')
for (id=0; id<posts.length ; id++) {
    console.log(id, posts[id].dataset['id']);
    posts_list[posts[id].dataset['id']] = new Post(id);
}

const url = window.location.href
console.log('url:', url)

var temp_url = url.replace('forum','forum-records')
console.log('temp_url:', temp_url)
var posts = []
fetch(temp_url)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            posts.push(data) 
        })
        .catch(error => console.log(error));