tagManager = (() => {
    // Private variables
    let existingTags = [];
    let newTags = [];

    // DOM Elements
    const elements = {
        tagSelect: document.getElementById('tag-select'),
        newTagInput: document.getElementById('new-tag'),
        selectedTagsContainer: document.getElementById('selected-tags'),
        existingTagsInput: document.getElementById('existing-tags-input'),
        newTagsInput: document.getElementById('new-tags-input')
    };

    // Initialize the component
    function init() {
        elements.tagSelect.addEventListener('change', handleTagSelection);
        elements.newTagInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addNewTag();
            }
        });

        // Initialize existing tags from the server-rendered content
        const initialTagElements = elements.selectedTagsContainer.querySelectorAll('[data-tag-id]');
        existingTags = Array.from(initialTagElements).map(tag => tag.dataset.tagId);

        // Update hidden input with initial values
        elements.existingTagsInput.value = existingTags.join(',');
    }

    function handleTagSelection() {
        const selectedOption = elements.tagSelect.options[elements.tagSelect.selectedIndex];
        const tagId = selectedOption.value;

        if (tagId && !existingTags.includes(tagId)) {
            existingTags.push(tagId);
            addTagElement(selectedOption.text, tagId, true);
            updateHiddenInputs();
        }
        elements.tagSelect.value = ''; // Reset selection
    }

    function addNewTag() {
        const newTag = elements.newTagInput.value.trim();

        if (newTag && !newTags.includes(newTag)) {
            newTags.push(newTag);
            addTagElement(newTag, newTag, false);
            updateHiddenInputs();
            elements.newTagInput.value = '';
        }
    }

    function removeTag(tagId) {
        existingTags = existingTags.filter(id => id !== tagId);
        const tagElement = elements.selectedTagsContainer.querySelector(`[data-tag-id="${tagId}"]`);
        if (tagElement) {
            tagElement.remove();
        }
        updateHiddenInputs();
    }

    function removeNewTag(tag) {
        newTags = newTags.filter(t => t !== tag);
        const tagElement = elements.selectedTagsContainer.querySelector(`[data-tag-id="${tag}"]`);
        if (tagElement) {
            tagElement.remove();
        }
        updateHiddenInputs();
    }

    function updateHiddenInputs() {
        elements.existingTagsInput.value = existingTags.join(',');
        elements.newTagsInput.value = newTags.join(',');
    }

    function addTagElement(text, value, isExisting) {
        const tagElement = document.createElement('span');
        tagElement.className = 'px-3 py-1 bg-gray-300 rounded-lg flex items-center';
        tagElement.dataset.tagId = value;

        tagElement.innerHTML = `
            <span>${text}</span>
            <button type="button" 
                    class="text-red-600 font-bold ml-2"
                    onclick="tagManager.${isExisting ? 'removeTag' : 'removeNewTag'}('${value}')">&times;</button>
        `;

        elements.selectedTagsContainer.appendChild(tagElement);
    }

    // Public API
    return {
        init,
        addNewTag,
        removeTag,
        removeNewTag,
        getSelectedTags: () => ({
            existing: existingTags,
            new: newTags
        })
    };
})();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', tagManager.init);