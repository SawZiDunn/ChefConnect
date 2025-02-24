const ingredientManager = (() => {
    // Private variables
    let ingredients = [];

    // DOM Elements
    const elements = {
        form: document.getElementById('ingredient-form'),
        ingredientSelect: document.getElementById('ingredient-select'),
        newIngredientInput: document.getElementById('new-ingredient'),
        quantityInput: document.getElementById('quantity'),
        unitsSelect: document.getElementById('units'),
        addButton: document.getElementById('add-ingredient'),
        selectedIngredientsContainer: document.getElementById('selected-ingredients'),
        existingIngredientsInput: document.getElementById('existing-ingredients-input'),
        newIngredientsInput: document.getElementById('new-ingredients-input'),
        quantitiesInput: document.getElementById('quantities-input'),
        unitsInput: document.getElementById('units-input')
    };

    // Initialize the component
    function init() {
        if (!elements.form) return; // Exit if form not found

        // Set up event listeners
        elements.addButton.addEventListener('click', handleAddIngredient);
        elements.newIngredientInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleAddIngredient();
            }
        });
        elements.form.addEventListener('submit', handleSubmit);

        // Load initial ingredients
        loadInitialIngredients();

        // Initial update of hidden inputs
        updateHiddenInputs();
    }

    function loadInitialIngredients() {
        const ingredientElements = elements.selectedIngredientsContainer.querySelectorAll('[data-ingredient-id]');

        ingredientElements.forEach(element => {
            const id = element.dataset.ingredientId;
            const text = element.querySelector('span').textContent;
            const [name, quantityUnit] = text.split(' - ');
            const [quantity, unit] = quantityUnit.split(' ');


            ingredients.push({
                id: id,
                name: name.trim(),
                quantity: quantity,
                unit: unit,
                isNew: false
            });

            // Add remove button functionality
            const removeButton = element.querySelector('.remove-ingredient');
            if (removeButton) {
                removeButton.addEventListener('click', () => removeIngredient(element));
            }
        });
    }

    function handleAddIngredient() {
        const selectedOption = elements.ingredientSelect.options[elements.ingredientSelect.selectedIndex];
        const newIngredientName = elements.newIngredientInput.value.trim();
        const quantity = elements.quantityInput.value.trim();
        const unit = elements.unitsSelect.value;

        if (!quantity) {
            alert('Please enter a quantity');
            return;
        }

        if (selectedOption.value) {
            // Adding existing ingredient
            addIngredient({
                id: selectedOption.value,
                name: selectedOption.text,
                quantity: quantity,
                unit: unit,
                isNew: false
            });
        } else if (newIngredientName) {
            // Adding new ingredient
            addIngredient({
                name: newIngredientName,
                quantity: quantity,
                unit: unit,
                isNew: true
            });
        } else {
            alert('Please select an ingredient or enter a new one');
            return;
        }

        resetInputs();
    }

    function addIngredient(ingredientData) {
        // Check if ingredient already exists
        const exists = ingredients.some(i =>
            (i.isNew && i.name.toLowerCase() === ingredientData.name.toLowerCase()) ||
            (!i.isNew && i.id === ingredientData.id)
        );

        if (exists) {
            alert('This ingredient is already added');
            return;
        }

        ingredients.push(ingredientData);
        renderIngredient(ingredientData);
        updateHiddenInputs();
    }

    function renderIngredient(ingredientData) {
        const div = document.createElement('div');
        div.className = 'flex justify-between items-center p-2 border rounded-lg bg-white';
        div.dataset.ingredientId = ingredientData.isNew ? ingredientData.name : ingredientData.id;

        // Get the display text for the unit using querySelector
        const unitDisplay = elements.unitsSelect.querySelector(`option[value="${ingredientData.unit}"]`)?.text || ingredientData.unit;

        div.innerHTML = `
        <span class="text-sm sm:text-base">${ingredientData.name} - ${ingredientData.quantity} ${unitDisplay}</span>
         <button type="button" class="remove-instruction text-red-500 hover:text-red-700 remove-ingredient">
                                        ×
         </button>
    `;

        // Add event listener to remove button
        const removeButton = div.querySelector('.remove-ingredient');
        removeButton.addEventListener('click', () => removeIngredient(div));

        elements.selectedIngredientsContainer.appendChild(div);
    }

    function removeIngredient(element) {
        const id = element.dataset.ingredientId;
        ingredients = ingredients.filter(i =>
            (i.isNew ? i.name !== id : i.id !== id)
        );
        element.remove();
        updateHiddenInputs();
    }

    function updateHiddenInputs() {
        const existing = ingredients.filter(i => !i.isNew);
        const newItems = ingredients.filter(i => i.isNew);

        elements.existingIngredientsInput.value = existing.map(i => i.id).join(',');
        elements.newIngredientsInput.value = newItems.map(i => i.name).join(',');
        elements.quantitiesInput.value = ingredients.map(i => i.quantity).join(',');
        elements.unitsInput.value = ingredients.map(i => i.unit).join(',');
    }

    function resetInputs() {
        elements.ingredientSelect.value = '';
        elements.newIngredientInput.value = '';
        elements.quantityInput.value = '';
        elements.unitsSelect.selectedIndex = 0;
    }

    function handleSubmit(e) {
        if (ingredients.length === 0) {
            e.preventDefault();
            alert('Please add at least one ingredient');
            return;
        }
    }

    // Public API
    return {
        init
    };
})();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', ingredientManager.init);