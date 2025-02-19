document.addEventListener("DOMContentLoaded", function () {
    let existingTags = [];  // List for existing categories
    let newTags = [];  // List for new categories

    function addNewTag() {
        let newTagInput = document.getElementById("new-tag");
        let newTag = newTagInput.value.trim();

        // Add new category if it's not empty and not already in the list
        if (newTag !== "" && !newTags.includes(newTag)) {
            newTags.push(newTag);  // Add to the new tag list
            updateTags();  // Update the displayed tag
            newTagInput.value = "";  // Clear the input field
        }
    }

    // Event listener for selecting tags from the dropdown
    document.getElementById("tag-select").addEventListener("change", function () {
        let selectedOption = this.options[this.selectedIndex];
        let tagId = selectedOption.value;

        if (tagId && !existingTags.includes(tagId)) {
            existingTags.push(tagId);  // Add to the selected categories list
            updateTags();  // Update the displayed categories
        }
    });

    // Function to update the displayed tags
    function updateTags() {
        let selectedContainer = document.getElementById("selected-tags");
        selectedContainer.innerHTML = "";  // Clear the existing categories

        // Display the selected categories (both new and existing)
        existingTags.forEach(tagId => {
            let categoryTag = document.createElement("span");
            categoryTag.classList.add("px-3", "py-1", "bg-gray-300", "rounded-lg", "flex", "items-center", "space-x-2");

            let tagName = document.querySelector(`#tag-select option[value="${tagId}"]`).text;
            categoryTag.innerHTML = `
                <span>${tagName}</span>
                <button type="button" class="text-red-600 font-bold ml-2" onclick="removeTag('${tagId}')">&times;</button>
            `;

            selectedContainer.appendChild(categoryTag);
        });

        // Display the new categories
        newTags.forEach(tag => {
            let categoryTag = document.createElement("span");
            categoryTag.classList.add("px-3", "py-1", "bg-gray-300", "rounded-lg", "flex", "items-center", "space-x-2");

            categoryTag.innerHTML = `
                <span>${tag}</span>
                <button type="button" class="text-red-600 font-bold ml-2" onclick="removeNewTag('${tag}')">&times;</button>
            `;

            selectedContainer.appendChild(categoryTag);
        });

        // Update hidden input fields
        document.getElementById("existing-tags-input").value = existingTags.join(",");
        document.getElementById("new-tags-input").value = newTags.join(",");
        console.log(existingTags);
        console.log(newTags);
    }

    // Function to remove a category from the list of selected categories
    window.removeTag = function (tagId) {
        existingTags = existingTags.filter(id => id !== tagId);
        updateTags();  // Update the displayed categories
    };

    // Function to remove a new category from the list
    window.removeNewTag = function (tag) {
        newTags = newTags.filter(current_tag => current_tag !== tag);
        updateTags();  // Update the displayed tags
    };

    // Expose addNewTag to the global scope for the button click
    window.addNewTag = addNewTag;
});
