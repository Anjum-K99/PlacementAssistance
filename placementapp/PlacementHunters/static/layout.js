window.onscroll = function() {scrollbar()};

function scrollbar() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = scrolled + "%";
} 

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