function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function like(event) {
    try {
        // Prevent double-clicking
        const likeButton = event.currentTarget;
        likeButton.disabled = true;

        const recipeId = document.querySelector('#recipe_id').value;

        const likeCount = document.getElementById('like-count');

        // Show loading state
        const originalText = likeButton.textContent;
        likeButton.textContent = '...';

        const response = await fetch(`/interactions/like/${recipeId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json()

        // Update button text and state
        likeButton.textContent = data.liked ? "❤️ Unlike" : "🤍 Like";

        // Optional: Add visual feedback
        if (data.liked) {
            likeButton.classList.add('text-red-500');
            likeButton.classList.remove('text-gray-500');
        } else {
            likeButton.classList.add('text-gray-500');
            likeButton.classList.remove('text-red-500');
        }

    } catch (error) {
        console.error('Error:', error);
        // Show error message to user
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
            errorMessage.textContent = 'Failed to update like status. Please try again.';
            errorMessage.classList.remove('hidden');
            setTimeout(() => {
                errorMessage.classList.add('hidden');
            }, 3000);
        }
    } finally {
        // Re-enable button
        likeButton.disabled = false;
    }
}

// Add event listener
document.querySelector('#like-button').addEventListener('click', like);