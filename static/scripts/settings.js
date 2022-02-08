function redirect(){
    let origin = window.location.origin
    let urls = {"profile": origin + "/accounts/settings/profile", 
                "authentication": origin + "/accounts/settings/authentication", 
                "delete_account": origin + "/accounts/settings/delete_account",
                "update": origin + `/community/${window.location.pathname.split("/")[2]}/update/`,
                "delete_community": origin + `/community/${window.location.pathname.split("/")[2]}/delete/`
            }

    let value = document.getElementById("select-field").value
    window.location.href = urls[value]
}