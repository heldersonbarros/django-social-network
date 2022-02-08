var page = 2;
var has_next = true;
const postsDiv = document.getElementById("posts");
const origin = window.location.origin

const postTemplate = `
<div class="post">
    <div class="title-div">
        <a class="post-title" href="">Title</a>
    </div>

<img src="" alt="">
<ul>
    <li><a href="" class="post-username" style="color: black;">Username</a></li>
</ul>

<div class="post-buttons" id="like-form">
</div>
</div>
`;

window.addEventListener("scroll", () => {
    if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
        if (has_next){
            getPost();
        }
    }
})

async function getPost(){
    const posts = await fetch(`${window.location.href}?page=${page}`, {
        headers:{
            'X-Requested-With': 'XMLHttpRequest', 
            'Content-Type': 'application/json', 'Accept': 'application/json'
        }
    });
    
    if (!posts.ok){
        has_next = false;
        throw new Error("HTTP status " + posts.status);
    }

    const response_json = await posts.json();
    postsJson = response_json.posts

    has_next = response_json.has_next

    page +=1

    for(var i=0; i<postsJson.length; i++){
        let post = postsJson[i]
        
        const parser = new DOMParser();
        const parsedDocument = parser.parseFromString(postTemplate, 'text/html');
        
        title = parsedDocument.getElementsByClassName("post-title")[0];
        title.textContent = post['title']
        title.href = `${origin}/post/${post['id']}`;

        if (post['owner']){
            delete_button = document.createElement("a")
            delete_button.href = `${origin}/post/${post['id']}/delete`
            delete_button.textContent = "Delete"
            delete_button.className = "delete-button"
            parsedDocument.getElementsByClassName("title-div")[0].appendChild(delete_button)
        }

        img = parsedDocument.querySelector("img");
        img.src = origin.concat(post['image']);

        username = parsedDocument.getElementsByClassName("post-username")[0];
        username.innerHTML = post['user']['username'];

        if (post['community']){
            community_li = document.createElement("li")
            community_a = document.createElement("a")
            community_a.href = `${origin}/community/${post['community']['id']}`
            community_a.textContent = post['community']['title']
            community_li.appendChild(community_a)
            parsedDocument.querySelector("ul").appendChild(community_li)
        }

        like_button = document.createElement("a")
        like_button.className = `js-like-button ${post['liked'] == true ? `liked`: `like-button`}`
        like_button.setAttribute("post_id", post['id'])
        like_button.setAttribute("id", `like${post['id']}`)
        like_button.textContent = post["like_count"]
        parsedDocument.getElementsByClassName("post-buttons")[0].appendChild(like_button)

        comments = document.createElement("a")
        comments.className = "post-button"
        comments.href = `${origin}/post/${post['id']}#comments`
        comments.textContent = "Comments"
        parsedDocument.getElementsByClassName("post-buttons")[0].appendChild(comments)

        postsDiv.appendChild(parsedDocument.documentElement)
    }

}