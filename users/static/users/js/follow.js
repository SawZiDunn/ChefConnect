// Function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// for following page
function FollowingToggleFollow(userId, buttonElement) {
    // get follow-btn if buttonElement is not passed
    const followButton = buttonElement || document.getElementById("follow-button");
    const followerCount = document.getElementById(`follower-count-${userId}`);

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

            console.log(followerCount);

            if (data.following) {
                followButton.textContent = "Unfollow";
                followButton.className = "w-full sm:w-auto mt-3 sm:mt-0 px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-md hover:bg-gray-400";


                // console.log("followers", data.follower_count);
                // console.log("followings", data.following_count);
            } else {
                followButton.textContent = "Follow";
                followButton.className = "w-full sm:w-auto mt-3 sm:mt-0 px-2 py-1 bg-blue-600 text-white text-xs rounded-md hover:bg-blue-700"

            }

            // update follower-count
            followerCount.innerText = data.follower_count + ` ${data.follower_count > 1 ? 'followers' : 'follower'}`;
        })
        .catch(error => console.error("Error:", error));
}

// for profile page
function ProfileToggleFollow(userId) {
  
    const followButton = document.getElementById("follow-button");
    const followerCount = document.getElementById(`follower-count`);

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
                followButton.className = "w-full sm:w-auto px-4 py-2 text-sm bg-gray-200 text-gray-700 hover:bg-gray-400 rounded-md";


                // console.log("followers", data.follower_count);
                // console.log("followings", data.following_count);
            } else {
                followButton.textContent = "Follow";
                followButton.className = "w-full sm:w-auto px-4 py-2 text-sm bg-blue-600 text-white hover:bg-blue-700 rounded-md"

            }

            // update follower-count
            followerCount.innerText = data.follower_count;
        })
        .catch(error => console.error("Error:", error));
}
