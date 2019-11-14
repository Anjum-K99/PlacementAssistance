console.log("here");


$(".dropdown-toggle").click(function(){
    $(".to-expand").toggle();
});

var i = 0;
var txt = 'Job Hunters'; /* The text */
var speed = 100; /* The speed/duration of the effect in milliseconds */

function typeWriter() {
    console.log('inside function')
  if (i < txt.length) {
    document.getElementById("heading-title").innerHTML += txt.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

function openForm() {
    document.getElementById("loginPopup").style.display="block";
  }
  
function closeForm() {
  document.getElementById("loginPopup").style.display= "none";
}
  // When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  var modal = document.getElementById('loginPopup');
  if (event.target == modal) {
    closeForm();
  }
}