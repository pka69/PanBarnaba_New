const key = document.getElementById("key")
const method = document.getElementById("method")
const encrypt = document.getElementById("encrypt")
const quotation = document.getElementById("game_id")
const answer = document.getElementById("answer")
const wrong = document.getElementById("wrong")

answer.addEventListener("change", function(){
    var data = {
        id: quotation.outerText, 
        method: method.outerText,
        key: key.outerText,
        answer: answer.value,
        // csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
    }
    const temp_url = '/encrypt/check_answer_is_correct/'  // + quotation.outerText + '/' + method.outerText + '/' + key.outerText + '/' + answer.value +"/"
    console.log(temp_url)
    console.log('data:', data)
    fetch(temp_url,
        {method:'POST',
        headers: {'Content-Type': 'application/json',
                    // 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
                },
        body: JSON.stringify(data)
        }
    )
        .then(response=> response.json())
            .then(data =>{
                console.log('response:',data)
                if (data["status"] == "success") {
                    finish.innerText = 1
                    wrong.classList.add("d-none")
                }
                else  {
                    console.log("błąd")
                    wrong.classList.remove("d-none")
                }
            })
            .catch(error => console.log(error));
})