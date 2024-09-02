const btn = document.getElementById("cross");
const be_removed = document.getElementById("signup");
const create = document.getElementById("createaccount")
btn.addEventListener("click", function() {
    be_removed.style.display="none";
});
create.addEventListener("click", function(){
    be_removed.style.display="flex";
});
