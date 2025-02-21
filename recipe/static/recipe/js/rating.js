function setRating(rating) {
    // Update hidden input
    document.getElementById('rating-input').value = rating;

    // Update star colors
    const stars = document.querySelectorAll('.star-btn');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('text-gray-300');
            star.classList.add('text-yellow-400');
        } else {
            star.classList.remove('text-yellow-400');
            star.classList.add('text-gray-300');
        }
    });
}