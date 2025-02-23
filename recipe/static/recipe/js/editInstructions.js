const instructionManager = (() => {
    // Private variables
    let instructions = [];
    let currentStepNumber = 1;

    // DOM Elements
    const elements = {
        form: document.getElementById('instruction-form'),
        instructionInput: document.getElementById('instruction-input'),
        addButton: document.getElementById('add-instruction'),
        instructionList: document.getElementById('instruction-list'),
        instructionsInput: document.getElementById('instructions-input')
    };

    function init() {
        if (!elements.form) return; // Exit if form not found

        // Set up event listeners
        elements.addButton.addEventListener('click', handleAddInstruction);
        elements.instructionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleAddInstruction();
            }
        });
        elements.form.addEventListener('submit', handleSubmit);

        // Load initial instructions
        loadInitialInstructions();
    }

    function loadInitialInstructions() {
        const instructionElements = elements.instructionList.querySelectorAll('.instruction-item');

        instructionElements.forEach(element => {
            const text = element.querySelector('.instruction-text').textContent;
            instructions.push(text);

            // Add event listeners to existing buttons
            setupInstructionButtons(element);
        });

        currentStepNumber = instructions.length + 1;
        updateHiddenInput();
    }

    function handleAddInstruction() {
        const instructionText = elements.instructionInput.value.trim();

        if (!instructionText) {
            alert('Please enter an instruction');
            return;
        }

        addInstruction(instructionText);
        elements.instructionInput.value = '';
        elements.instructionInput.focus();
    }

    function addInstruction(text) {
        instructions.push(text);
        renderInstruction(text, instructions.length);
        updateHiddenInput();
        currentStepNumber++;
    }

    function renderInstruction(text, stepNumber) {
        const div = document.createElement('div');
        div.className = 'instruction-item flex items-start space-x-4 p-2 border rounded-lg bg-white';

        div.innerHTML = `
            <span class="instruction-number font-semibold min-w-[2rem]">${stepNumber}.</span>
            <p class="instruction-text flex-grow">${text}</p>
            <div class="flex space-x-2">
                <button type="button" class="move-up text-gray-600 hover:text-gray-900 px-2">↑</button>
                <button type="button" class="move-down text-gray-600 hover:text-gray-900 px-2">↓</button>
                <button type="button" class="remove-instruction text-red-500 hover:text-red-700">×</button>
            </div>
        `;

        setupInstructionButtons(div);
        elements.instructionList.appendChild(div);
    }

    function setupInstructionButtons(element) {
        element.querySelector('.remove-instruction').addEventListener('click', () => removeInstruction(element));
        element.querySelector('.move-up').addEventListener('click', () => moveInstruction(element, 'up'));
        element.querySelector('.move-down').addEventListener('click', () => moveInstruction(element, 'down'));
    }

    function removeInstruction(element) {
        const index = Array.from(elements.instructionList.children).indexOf(element);
        instructions.splice(index, 1);
        element.remove();
        updateStepNumbers();
        updateHiddenInput();
        currentStepNumber--;
    }

    function moveInstruction(element, direction) {
        const index = Array.from(elements.instructionList.children).indexOf(element);

        if (direction === 'up' && index > 0) {
            // Move up
            const temp = instructions[index];
            instructions[index] = instructions[index - 1];
            instructions[index - 1] = temp;
            elements.instructionList.insertBefore(element, element.previousElementSibling);
        } else if (direction === 'down' && index < instructions.length - 1) {
            // Move down
            const temp = instructions[index];
            instructions[index] = instructions[index + 1];
            instructions[index + 1] = temp;
            elements.instructionList.insertBefore(element.nextElementSibling, element);
        }

        updateStepNumbers();
        updateHiddenInput();
    }

    function updateStepNumbers() {
        elements.instructionList.querySelectorAll('.instruction-item').forEach((item, index) => {
            item.querySelector('.instruction-number').textContent = `${index + 1}.`;
        });
    }

    function updateHiddenInput() {
        elements.instructionsInput.value = JSON.stringify(instructions);
    }

    function handleSubmit(e) {
        if (instructions.length === 0) {
            e.preventDefault();
            alert('Please add at least one instruction');
            return;
        }
    }

    // Public API
    return {
        init
    };
})();

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', instructionManager.init);