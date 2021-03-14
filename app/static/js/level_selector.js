levels = document.querySelectorAll("[id^='level_']")
console.log(levels)

function changeLevel(target) {
    console.log(target.name)
    target.checked = true;
    
    for (item of levels) {
        if (item != target) {
            item.checked = false;
        }
    }
    const level = target.name.split('_');
    document.cookie = "level=" + level[1];
}

levels.forEach((item) => {
    item.addEventListener('change', function(event){
        event.preventDefault();
        changeLevel(this)
        })
})