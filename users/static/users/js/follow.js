// Function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function toggleFollow(userId) {
    const followButton = document.getElementById("follow-button");

    if (!followButton) return;

    fetch(`/interactions/follow/${userId}/`, {  // URL should match your Django view
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django security
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.following) {
                followButton.textContent = "Unfollow";
                followButton.className = "px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300";


                console.log("followers", data.follower_count);
                console.log("followings", data.following_count);
            } else {
                followButton.textContent = "Follow";
                followButton.className = "px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"


                console.log("followers", data.follower_count);
                console.log("followings", data.following_count);
            }

            document.getElementById('follower_count').textContent = data.follower_count;
        })
        .catch(error => console.error("Error:", error));
}
