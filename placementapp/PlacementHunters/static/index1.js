console.log("here");
$(document).ready(function(){
    $(window).scroll(function(){
        if($(window).scrollTop()){
            $('.main-nav').css({"background-color":"rgba(100,100,100,0.7)"});
            $('.main-nav .nav-btn').css({"color":"white"});
            $('.main-nav .nav-btn').css({"background-color":"rgba(0,0,0,0.25)"});
        }
        else{
            $('.main-nav').css({"background-color":"transparent"});
            $('.main-nav .nav-btn').css({"color":"black"});
        }
    })
    typeWriter();
})

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