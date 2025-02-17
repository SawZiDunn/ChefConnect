document.addEventListener('DOMContentLoaded', function () {
    // Instruction Elements
    const instructionInput = document.getElementById('instruction-input');
    const instructionList = document.getElementById('instruction-list');
    const addInstructionButton = document.getElementById('add-instruction');
    let stepCount = 1;


    addInstructionButton.addEventListener('click', function () {
        const instructionText = instructionInput.value.trim();

        if (!instructionText) {
            alert('Please enter an instruction');
            return;
        }

        // Create instruction element
        const instructionDiv = document.createElement('div');
        instructionDiv.className = 'flex justify-between items-start p-2 border rounded-lg bg-white';

        instructionDiv.innerHTML = `
            <div class="flex-1">
                <span class="font-medium">Step ${stepCount}:</span>
                <p class="mt-1">${instructionText}</p>
                <input type="hidden" name="instructions[]" value="${instructionText}">
            </div>
            <button type="button" class="bg-red-500 text-white px-3 py-1 rounded ml-4 remove-instruction">Remove</button>
        `;

        instructionList.appendChild(instructionDiv);
        stepCount++;

        // Reset input field
        instructionInput.value = '';
    });

// Remove instruction & update step numbers
    instructionList.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-instruction')) {
            e.target.closest('div').remove();
            stepCount--;

            // Update step numbers
            const steps = instructionList.querySelectorAll('.font-medium');
            steps.forEach((step, index) => {
                step.textContent = `Step ${index + 1}:`;
            });
        }
    });
})