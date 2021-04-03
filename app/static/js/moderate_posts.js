var ModalForm = document.getElementById('AddModPost')

var pictureType = document.getElementsByName("pictureType")
console.log(pictureType.length)

var pictureLocation = document.getElementsByName("pictureLocation")
console.log(pictureLocation.length)
var ID_list = document.getElementsByName("post_ID")
console.log(ID_list.length)

function pictureTypeChange() {
    console.log(pictureType[0].checked, pictureType[1].checked)
    pictureType.forEach((item, id) => {
        if (item.checked == true) {
            pictureLocation[id].classList.remove("d-none")
        }
        else {
            pictureLocation[id].classList.add("d-none")
        }
    })
    // if (pictureType[0]checked == true) {
    //     pictureType[0]checked = false;
    //     pictureType[1]checked = true;
    // }
    // else {
    //     pictureType[0]checked = true;
    //     pictureType[1]checked = false;
    // }
}

pictureType.forEach(item => item.addEventListener('change', pictureTypeChange))

ModalForm.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever')
    var post_data = button.dataset
    
    if (! (post_data["id"])) {
        return
    }
    var modal_id = ModalForm.querySelector("#id")
    var modal_subgroup = ModalForm.querySelector('#subgroup')
    var modal_stage = ModalForm.querySelectorAll('#stage')
    var modal_content = ModalForm.querySelector('#content')
    var modal_external_link = ModalForm.querySelector('#external_link')
    console.log(modal_stage)
    modal_id.value = parseInt(post_data["id"])
    modal_subgroup.value = post_data["subgroup"]
    for (var item of modal_stage) {
        if (item ===post_data['stage']){
            item.checked = true
        }
        else {
            item.checked = false
        }
    }
    modal_content.value = post_data['content']

    modal_external_link.value = post_data['external_link']
    // console.log(post_data['picture'].startsWith('http'))
    // if (post_data['picture'].startsWith('http')) {
        ModalForm.querySelector('#pictureType1').checked = false 
        ModalForm.querySelector('#pictureType2').checked = true 
        ModalForm.querySelector('#picture').value = post_data['picture']
    // }
    // else {
    //     ModalForm.querySelector('#pictureType1').checked = true 
    //     ModalForm.querySelector('#pictureType2').checked = false 
    //     ModalForm.querySelector('#pictureFile').value = post_data['picture']
    // }
    
})
