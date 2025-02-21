// Function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function saveToggle(recipeId) {
    const saveButton = document.getElementById("save-button");

    if (!saveButton) return;

    fetch(`/recipe/save/${recipeId}/`, {  // URL should match your Django view
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django security
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            saveButton.textContent = data.isSaved ? "Unsave" : "Save"
        })
        .catch(error => console.error("Error:", error));
}
