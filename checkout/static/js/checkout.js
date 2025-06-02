// JavaScript for Checkout Page

document.addEventListener('DOMContentLoaded', function () {
    // Handle dynamic display of password fields
    const createProfileCheckbox = document.getElementById('create-profile');
    const passwordFields = document.getElementById('password-fields');

    if (createProfileCheckbox && passwordFields) {
        createProfileCheckbox.addEventListener('change', function () {
            if (createProfileCheckbox.checked) {
                passwordFields.style.display = 'block';
                passwordFields.setAttribute('aria-expanded', 'true');
            } else {
                passwordFields.style.display = 'none';
                passwordFields.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Additional checkout-related JavaScript can go here
    // Example: Stripe integration logic
});