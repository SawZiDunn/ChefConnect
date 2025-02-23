// Function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function toggleFollow(userId) {
    const followButton = document.getElementById("follow-button");

    if (!followButton) return;

    fetch(`/interactions/user/${userId}/follow/`, {  // URL should match your Django view
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
                followButton.className = "bg-gray-200 text-gray-700 px-3 py-1 rounded-md hover:opacity-80";


            } else {
                followButton.textContent = "Follow";
                followButton.className = "bg-blue-600 text-white px-3 py-1 rounded-md hover:opacity-80"


            }

        })
        .catch(error => console.error("Error:", error));
}
