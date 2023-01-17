function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('click', function(event){
	if (event.target.classList.contains("js-like-button")){
		like_post(event.target)
	}

	if (event.target.classList.contains("js-follow-button")) {
		follow_user(event.target)
	}

	if (event.target.classList.contains("js-join-button")) {
		join_community(event.target)
	}

})

async function like_post(button){
	const response = await fetch(`/like_post`, 
			{
				headers:{'X-CSRFToken': csrftoken}, 
				method: "POST", body: JSON.stringify({'post_id':button.getAttribute("post_id")})
			});
    
	const response_json = await response.json();

	if(response_json["added"] == true){
		button.innerHTML = `<i class="fa-solid fa-heart fa-lg"></i> ${response_json.count}`
	} else{
		button.innerHTML = `<i class="fa-regular fa-heart fa-lg"></i> ${response_json.count}`
	}
}

async function join_community(button){
	const response = await fetch(`${window.location.origin}/community/join/`, 
	{
		headers:{'X-CSRFToken': csrftoken}, 
		method: "POST", body: JSON.stringify({'community_id':button.getAttribute("community_id")})
	});

	const response_json = await response.json();

	if (response_json.added == true){
		button.innerText = "Leave"
	} else{
		button.innerText = "Join";
	}

	if(window.location.href.indexOf("all") > -1){
		button.classList.toggle('follow-button')
		button.classList.toggle('unfollow-button')
	} else{
		button.classList.toggle('btn-light')
		button.classList.toggle('btn-dark')
	}

	document.getElementById(`community-followers-${button.getAttribute("community_id")}`).innerText = `${response_json.count} Followers`
}

async function follow_user(button){
	const response = await fetch(`http://${window.location.host}/accounts/profile/follow/`, 
			{
				headers:{'X-CSRFToken': csrftoken},
				method: "POST", body: JSON.stringify({'user_id':button.getAttribute("user_id")})
			});
	
	const response_json = await response.json();

	if (response_json.added == true){
			button.innerText = "Unfollow"
	} else{
			button.innerText = "Follow"
	}

	button.classList.toggle('unfollow-button')
	button.classList.toggle('follow-button')
	document.getElementById("followers-count").innerText = `${response_json.count}`
}