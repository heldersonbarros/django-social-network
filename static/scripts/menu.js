const dropdown = document.getElementById("dropdown");
const side_nav = document.querySelector(".menu-hidden-bar");
const search_form = document.getElementById("search-form");
const profile_image = document.getElementsByClassName("profile-image")[0];
const back_icon = document.getElementById("back-icon");
const theme_toggle = document.getElementById("theme-toggle");
const theme = window.localStorage.getItem("theme");
const burger = document.getElementById("burger")

if (theme == "dark") {
    document.body.classList.add("dark");
    theme_toggle.checked = true;
}

document.addEventListener('click', function(event){
    if (event.target.id == "image"){
        dropdown.style.display = "flex";
    }
    else if (event.target.classList.contains("line") || event.target.classList.contains("burger")){
        side_nav.classList.toggle("nav-active");
    }
    else if (event.target.id == "search" || event.target.id == "back-icon"){
        back_icon.classList.toggle("back-icon-disabled");
        profile_image.classList.toggle("profile-image-active");
        search_form.classList.toggle("search-active");
        burger.classList.toggle("burger");
    }
    else if (event.target.classList.contains("slider") || event.target.tagName == "INPUT"){
        if (event.target.classList.contains("slider")){
            document.body.classList.toggle("dark");
            if (theme == "dark") {
                window.localStorage.setItem("theme", "light");
            } else{
                window.localStorage.setItem("theme", "dark");
            }
        }
    }
    else{
        document.getElementById("dropdown").style.display = "none";
    }
})