// JavaScript for Checkout Page

document.addEventListener('DOMContentLoaded', function () {
    // Handle dynamic display of password fields
    const createProfileCheckbox = document.getElementById('create-profile');
    const passwordFields = document.getElementById('password-fields');

    if (createProfileCheckbox) {
        createProfileCheckbox.addEventListener('change', function () {
            if (createProfileCheckbox.checked) {
                passwordFields.style.display = 'block';
            } else {
                passwordFields.style.display = 'none';
            }
        });
    }

    // Additional checkout-related JavaScript can go here
    // Example: Stripe integration logic
});