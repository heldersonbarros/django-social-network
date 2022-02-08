let page = 2;
var commentDiv = document.getElementById("comments");
let has_next = true;
const template = `
<div class="comment" id="comments">
<img class="rounded-image" src="" alt="">
<div class="comment-body">
    <a class="comment-username" href="">Username</a>
    <p>Text</p>
</div>
</div>`

window.addEventListener("scroll", () => {
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
        if (has_next){
            getComments();
        }
    }
})

async function getComments(){
    const comments = await fetch(`${window.location.origin}${window.location.pathname}/comments?page=${page}`, {
        headers:{'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json', 'Accept': 'application/json'}
    });
    
    if (!comments.ok){
        has_next = false;
        throw new Error("HTTP status " + comments.status);
    }

    const response_json = await comments.json();

    commentsJson = response_json.comments
    has_next = response_json.has_next

    page +=1

    for(var i=0; i<commentsJson.length; i++){
        let comment = commentsJson[i]

        const parser = new DOMParser();
        const parsedDocument = parser.parseFromString(template, 'text/html');
        
        comment_profile_image = parsedDocument.querySelector("img");
        comment_profile_image.src = comment['user']['image'];

        username = parsedDocument.getElementsByClassName("comment-username")[0]
        username.href = `${window.location.origin}/accounts/profile/${comment["user"]["username"]}`
        username.textContent = comment['user']['username']

        text = parsedDocument.querySelector("p")
        text.textContent = comment['text']

        commentDiv.appendChild(parsedDocument.documentElement)
    }

}