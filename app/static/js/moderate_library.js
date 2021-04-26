var ModalForm = document.getElementById('AddModPost')

ModalForm.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    var lib_data = button.dataset
    
    if (! (lib_data["id"])) {
        return
    }
    console.log(ModalForm.querySelector('#next').value)
    const modal_text = {
        'id':'',
        'moderator':'',
        'email':'',
        'www':'',
        'telefon':'',
        'salutation':'',
        'notes':'',
        'name':'',
        'city':'',
        'theme':'',
    }
    const modal_flags = {
        'ddk_kids':'',
        'ddk_adults':'',
        'ddk_young':'',
        'ddk_closed':'',
    }
    
    for (let key in modal_text) {
        modal_text[key] = lib_data[key]
        if (modal_text[key]) {  ModalForm.querySelector('#' + key).value = lib_data[key] }
    }
    for (let key in modal_flags) {
        modal_text[key] = (lib_data[key]=="True")?true:false
        if (modal_text[key]) {  ModalForm.querySelector('#' + key).checked =(lib_data[key]=="True")?true:false }
    }
    // ModalForm.querySelector('#lib_name').innerText = lib_data['name']
    console.log(modal_flags)
    console.log(modal_text)
    console.log(lib_data)
})
