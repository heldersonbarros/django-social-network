const dropdown = document.getElementById("dropdown");
const side_nav = document.querySelector(".menu-hidden-bar");
const search_form = document.getElementById("search-form");
const profile_image = document.getElementsByClassName("profile-image")[0];
const back_icon = document.getElementById("back-icon");

document.addEventListener('click', function(event){
    if (event.target.id == "image"){
        dropdown.style.display = "flex";
    }
    else if (event.target.classList.contains("line") || event.target.classList.contains("burger")){
        side_nav.classList.toggle("nav-active");
    }
    else if (event.target.id == "search" || event.target.id == "back-icon"){
        back_icon.classList.toggle("back-icon-active");
        profile_image.classList.toggle("profile-image-active");
        search_form.classList.toggle("search-active");
    }
    else{
        document.getElementById("dropdown").style.display = "none";
    }
})