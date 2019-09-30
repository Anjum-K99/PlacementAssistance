$(document).ready(function(){
    document.getElementById('job-seeker-profile').style.display = "block";//show profile page by default
    let page = document.getElementsByClassName("tablinks");
    page[0].className +=" active"
})

function openTab(evt,pageName){
    // Get all elements with class="tabcontent" and hide them
    let tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");//list of all elements that have the class of tablinks
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(pageName).style.display = "block";//show my page
    evt.currentTarget.className += " active";
}

// document.querySelector('.tablinks').onmousemove = (e) => {  
//     let x = e.pageX - e.target.offsetLeft;
//     let y = e.pageY - e.target.offsetTop;
//     e.target.style.setProperty('--x', `${ x }px`);
//     e.target.style.setProperty('--y', `${ y }px`);
   
//   }