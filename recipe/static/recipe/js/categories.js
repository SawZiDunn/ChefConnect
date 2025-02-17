document.addEventListener("DOMContentLoaded", function () {
    let existingCategories = [];  // List for existing categories
    let newCategories = [];  // List for new categories

    function addNewCategory() {
        let newCategoryInput = document.getElementById("new-category");
        let newCategory = newCategoryInput.value.trim();

        // Add new category if it's not empty and not already in the list
        if (newCategory !== "" && !newCategories.includes(newCategory)) {
            newCategories.push(newCategory);  // Add to the new categories list
            updateCategories();  // Update the displayed categories
            newCategoryInput.value = "";  // Clear the input field
        }
    }

    // Event listener for selecting categories from the dropdown
    document.getElementById("category-select").addEventListener("change", function () {
        let selectedOption = this.options[this.selectedIndex];
        let categoryId = selectedOption.value;

        if (categoryId && !existingCategories.includes(categoryId)) {
            existingCategories.push(categoryId);  // Add to the selected categories list
            updateCategories();  // Update the displayed categories
        }
    });

    // Function to update the displayed categories
    function updateCategories() {
        let selectedContainer = document.getElementById("selected-categories");
        selectedContainer.innerHTML = "";  // Clear the existing categories

        // Display the selected categories (both new and existing)
        existingCategories.forEach(categoryId => {
            let categoryTag = document.createElement("span");
            categoryTag.classList.add("px-3", "py-1", "bg-gray-300", "rounded-lg", "flex", "items-center", "space-x-2");

            let categoryName = document.querySelector(`#category-select option[value="${categoryId}"]`).text;
            categoryTag.innerHTML = `
                <span>${categoryName}</span>
                <button type="button" class="text-red-600 font-bold ml-2" onclick="removeCategory('${categoryId}')">&times;</button>
            `;

            selectedContainer.appendChild(categoryTag);
        });

        // Display the new categories
        newCategories.forEach(category => {
            let categoryTag = document.createElement("span");
            categoryTag.classList.add("px-3", "py-1", "bg-gray-300", "rounded-lg", "flex", "items-center", "space-x-2");

            categoryTag.innerHTML = `
                <span>${category}</span>
                <button type="button" class="text-red-600 font-bold ml-2" onclick="removeNewCategory('${category}')">&times;</button>
            `;

            selectedContainer.appendChild(categoryTag);
        });

        // Update hidden input fields
        document.getElementById("existing-categories-input").value = existingCategories.join(",");
        document.getElementById("new-categories-input").value = newCategories.join(",");
        console.log(existingCategories);
        console.log(newCategories);
    }

    // Function to remove a category from the list of selected categories
    window.removeCategory = function (categoryId) {
        existingCategories = existingCategories.filter(id => id !== categoryId);
        updateCategories();  // Update the displayed categories
    };

    // Function to remove a new category from the list
    window.removeNewCategory = function (category) {
        newCategories = newCategories.filter(cat => cat !== category);
        updateCategories();  // Update the displayed categories
    };

    // Expose addNewCategory to the global scope for the button click
    window.addNewCategory = addNewCategory;
});
