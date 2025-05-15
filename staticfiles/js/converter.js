    document.addEventListener('DOMContentLoaded', function () {
        const convertBtn = document.getElementById('convert-btn');
        const cmInput = document.getElementById('cm-input');
        const result = document.getElementById('result');

        if (!convertBtn || !cmInput || !result) {
            console.error('One or more elements are missing from the DOM.');
            return;
        }

        convertBtn.addEventListener('click', function () {
            const cmValue = parseFloat(cmInput.value);
            if (!isNaN(cmValue)&& cmValue > 0) {
                const inches = Math.floor(cmValue / 2.54); // Convert cm to inches & round down
                result.textContent = `You need a ${inches}-inch hurley.`;
                result.style.color = '#fff'; 
                cmInput.value = "";
            } else {
                result.textContent = 'Please enter a valid number.';
                result.style.color = '#ff0000';
            }
        });
    });