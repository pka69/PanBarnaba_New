var ModalForm = document.querySelector('#AddMod')
var ID_list = document.getElementsByName("quiz_ID")

ModalForm.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    var quiz_data = button.dataset
    console.log('quiz_data', quiz_data)
    if (! (quiz_data["id"])) {
        return
    }
    var modal_id = ModalForm.querySelector("#id")
    var modal_qgroup = ModalForm.querySelector('#qgroup')
    var modal_qlevel = ModalForm.querySelectorAll('#qlevel')
    console.log('qlevel', modal_qlevel)
    var modal_question = ModalForm.querySelector('#question')
    var modal_qtype = ModalForm.querySelectorAll('#qtype')
    console.log('qtype', modal_qtype)
    modal_id.value = parseInt(quiz_data["id"])
    modal_qgroup.value = quiz_data["qgroup"]
    for (var item of modal_qlevel) {
        if (item.value === quiz_data['qlevel']){
            item.checked = true
        }
        else {
            item.checked = false
        }
    }
    modal_question.value = quiz_data['question']
    for (var item of modal_qtype) {
        if (item.value === quiz_data['qtype']){
            item.checked = true
        }
        else {
            item.checked = false
        }
    }
    
})