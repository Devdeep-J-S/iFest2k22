/*const targetData = document.querySelector(".round-display-toggle");
const trigger = document.querySelector(".round-heading");
trigger.onclick = function(){
    if (targetData.style.display !== "none") {
        targetData.style.display = "none";
    }
    else {
        targetData.style.display = "block";
    }
};*/

function toggleDisplay(){
    arg = event.target.getAttribute('arg');
    const targetData = document.getElementById(arg);
      if (targetData.style.display !== "none") {
         targetData.style.display = "none";
     }
    else {
         targetData.style.display = "block";
     }

}
