let button = document.getElementById("cross");
let deleting_item = document.getElementById("message");
button.addEventListener("click", function(){
    deleting_item.remove();
    button.remove();
})