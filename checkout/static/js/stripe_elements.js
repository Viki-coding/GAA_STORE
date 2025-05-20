/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// Retrieve Stripe public key and client secret from the DOM
console.log("Stripe JS loaded");
const stripePublicKeyElement = document.getElementById('id_stripe_public_key');
const clientSecretElement = document.getElementById('id_client_secret');

if (!stripePublicKeyElement || !clientSecretElement) {
    console.error('Stripe public key or client secret is missing.');
    alert('An error occurred while loading the payment form. Please try again.');
}

const stripePublicKey = stripePublicKeyElement.textContent.trim();
const clientSecret = clientSecretElement.textContent.trim();

// Initialize Stripe
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

// Define custom styling for the card element
const style = {
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
const card = elements.create('card', { style: style });
card.mount('#card-element');

// Handle real-time validation errors on the card element
card.addEventListener('change', function (event) {
    const errorDiv = document.getElementById('card-errors');
    if (event.error) {
        const errorHtml = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = errorHtml;
    } else {
        errorDiv.textContent = '';
    }
});

const form = document.getElementById('checkout-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                // Optionally collect name, email, etc.
            }
        }
    }).then(function(result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            const errorDiv = document.getElementById('card-errors');
            errorDiv.textContent = result.error.message;
        } else {
            // The payment succeeded!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit(); // Optionally, submit the form or redirect
            }
        }
    });
});

const submitButton = document.getElementById('submit-button');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: form.name.value,
                email: form.email.value,
            }
        }
    }).then(function(result) {
        if (result.error) {
            const errorDiv = document.getElementById('card-errors');
            errorDiv.textContent = result.error.message;
            submitButton.disabled = false;
            submitButton.innerHTML = 'Complete Order';
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
