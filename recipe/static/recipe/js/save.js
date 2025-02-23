// Function to get CSRF token
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function saveToggle(recipeId, btnElement) {
    const saveButton = btnElement || document.getElementById("save-button");

    if (!saveButton) return;

    fetch(`/recipe/${recipeId}/save/`, {  // URL should match your Django view
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"), // CSRF token for Django security
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {
            saveButton.textContent = data.isSaved ? "Unsave" : "Save"

            if (data.isSaved) {
                saveButton.className = "flex items-center px-3 py-1 bg-gray-300 text-gray-700 rounded-md hover:opacity-80 justify-center"
            } else {
                saveButton.className = "flex items-center px-3 py-1 bg-blue-600 text-white rounded-md hover:opacity-80 justify-center"
            }
        })
        .catch(error => console.error("Error:", error));
}
