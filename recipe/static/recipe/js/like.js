function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function like(recipeId) {
    const like_button = document.querySelector('#like-button');
    const like_count = document.querySelector('#like-count');


    try {
        const response = await fetch(`/interactions/recipe/${recipeId}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django security
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`Response Status: ${response.status}`)
        }

        const data = await response.json()
        if (!data.isLiked) {
            like_button.innerHTML = "Like";

        } else {
            like_button.innerHTML = "Unlike";
    
        }

        like_count.textContent = data.total_likes;


    } catch (e) {
        console.error(e.message);
    }
}