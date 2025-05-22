/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// Retrieve Stripe public key and client secret from the DOM
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

if (!stripePublicKey || !clientSecret) {
    console.error('Stripe public key or client secret is missing.');
    alert('An error occurred while loading the payment form. Please try again.');
}

// Initialize Stripe
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Define custom styling for the card element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4',
        },
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545',
    },
};

// Create and mount the card element
var card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

var form = document.getElementById('checkout-form');
var submitButton = document.getElementById('submit-button');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Disable the submit button to prevent repeated clicks
    card.update({ 'disabled': true });
    $(submitButton).attr('disabled', true);
    $(submitButton).html('<span class="spinner-border spinner-border-sm"></span> Processing...');

   // confirm card payment 
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: form.name.value,
                email: form.email.value,
            }
        }
    }).then(function (result) {
        if (result.error) {
            // Display error message
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            $(errorDiv).html(html);

            // Re-enable card input and submit button
            card.update({ 'disabled': false });
            $(submitButton).attr('disabled', false);
            $(submitButton).html('Complete Order');
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                // Submit the form
                form.submit();
            }
        }
    });
});
