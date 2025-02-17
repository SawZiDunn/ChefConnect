document.addEventListener('DOMContentLoaded', function () {
    // Ingredient Elements
    const ingredientSelect = document.getElementById('ingredient-select');
    const newIngredient = document.getElementById('new-ingredient');
    const quantity = document.getElementById('quantity');
    const units = document.getElementById('units');
    const ingredientList = document.getElementById('ingredient-list');
    const addIngredientButton = document.getElementById('add-ingredient');


    // Clear other input when one is being used
    ingredientSelect.addEventListener('change', function () {
        if (this.value) newIngredient.value = '';
    });

    newIngredient.addEventListener('input', function () {
        if (this.value) ingredientSelect.value = '';
    });

    addIngredientButton.addEventListener('click', function () {
        const selectedIngredient = ingredientSelect.value;
        const newIngredientValue = newIngredient.value.trim();
        const quantityValue = quantity.value.trim();
        const unitsValue = units.value;

        if ((!selectedIngredient && !newIngredientValue) || !quantityValue) {
            alert('Please fill in all required fields');
            return;
        }

        // Get the ingredient name
        let ingredientName = newIngredientValue || ingredientSelect.options[ingredientSelect.selectedIndex].text;

        // Create ingredient element
        const ingredientDiv = document.createElement('div');
        ingredientDiv.className = 'flex justify-between items-center p-2 border rounded-lg bg-white';

        ingredientDiv.innerHTML = `
            <span>${ingredientName} - ${quantityValue} ${unitsValue}</span>
            <button type="button" class="bg-red-500 text-white px-3 py-1 rounded remove-ingredient">Remove</button>
            <input type="hidden" name="ingredients[]" value="${selectedIngredient}">
            <input type="hidden" name="new_ingredients[]" value="${newIngredientValue}">
            <input type="hidden" name="quantities[]" value="${quantityValue}">
            <input type="hidden" name="units[]" value="${unitsValue}">
        `;

        ingredientList.appendChild(ingredientDiv);

        // Reset fields
        ingredientSelect.value = '';
        newIngredient.value = '';
        quantity.value = '';
        units.value = 'g';
    });

    // Remove ingredient using event delegation
    ingredientList.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-ingredient')) {
            e.target.closest('div').remove();
        }
    });
})