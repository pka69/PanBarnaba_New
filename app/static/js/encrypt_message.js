const GADERYPOLUKI_key = document.getElementsByName('key')[0];
const emailBox = document.getElementsByName('emailBox')[0];
const method_select = document.getElementsByName('method_select')[0];
const method_list = document.getElementsByName('method_list');
const keys = document.getElementsByName('keys');
const to_encrypt = document.getElementsByName('to_encrypt')[0];
const submit = document.getElementsByName('submit')[0];
var method = '';
var key='';
method_select.addEventListener('change', function(event){
    for (item of method_list) {
        if (item.selected) {method = item.value}
    }
    if (method ===''){ return}
    method_select.disabled= true
    if (method ==="gaderypoluki") {
        GADERYPOLUKI_key.classList.remove('d-none')
    }
    else {
        emailBox.classList.remove('d-none')
    }
    document.getElementsByName('method_selected')[0].innerHTML = "Wybrano metodę: <b>" + method + "</b>"
    console.log(method)
    console.log(method_select)
})
GADERYPOLUKI_key.addEventListener('change', function(event) {
    for (item of keys) {
        if (item.selected) {key = item.value}
    }
    if (key ===''){ return}
    GADERYPOLUKI_key.disabled= true;
    emailBox.classList.remove('d-none')
    document.getElementsByName('method_selected')[0].innerHTML = "Wybrano metodę: <b>" + method + "</b>" + ", klucz szyfrowania: <b>" + key + "</b>";
})
emailBox.addEventListener('change', function() {
    emailBox.disabled = true
    to_encrypt.classList.remove('d-none')
    submit.classList.remove('d-none')
    document.getElementById('method_id').value = method
    document.getElementById('key_id').value = key
    console.log(document.getElementById('method_id').value, method)
    console.log(document.getElementById('key_id').value, key)
})

