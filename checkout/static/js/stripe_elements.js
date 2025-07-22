// 1) Grab the Stripe public key and client secret that Django embedded in the page
var stripePublicKey = JSON.parse(
    document.getElementById('id_stripe_public_key').textContent
);
var clientSecret = JSON.parse(
    document.getElementById('id_client_secret').textContent
);

if (!stripePublicKey || !clientSecret) {
    console.error('Stripe public key or client secret is missing.');
    alert('An error occurred while loading the payment form. Please try again.');
}

// 2) Initialize Stripe.js
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// 3) Define custom styling for the card element
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

// 4) Create and mount the Card Element
var card = elements.create('card', { style: style });
card.mount('#card-element');

// 5) Real-time validation for card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    var feedbackDiv = document.getElementById('card-feedback');

    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        errorDiv.innerHTML = html;
        feedbackDiv.textContent = '';  // clear any success msg
    } else {
        errorDiv.textContent = '';
        if (event.complete) {
            feedbackDiv.innerHTML = `
              <div class="alert alert-success py-1 px-2 small">
                <i class="fas fa-check-circle"></i> Card is valid. Processing payment...
              </div>
            `;
        } else {
            feedbackDiv.textContent = '';
        }
    }
});

// 6) Grab the form and submit button
var form = document.getElementById('checkout-form');
var submitButton = document.getElementById('submit-button');

// 7) Intercept form submission
form.addEventListener('submit', function(event) {
    event.preventDefault();

    // Disable card input and button to prevent multiple clicks
    card.update({ 'disabled': true });
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';

    // 8) Retrieve billing details
    var billingName  = document.getElementById('full_name').value;
    var billingEmail = document.getElementById('billing_email').value;

    // 9) Confirm the card payment with Stripe
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: billingName,
                email: billingEmail,
            }
        }
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var feedbackDiv = document.getElementById('card-feedback');
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            errorDiv.innerHTML = html;
            feedbackDiv.textContent = '';

            card.update({ 'disabled': false });
            submitButton.disabled = false;
            submitButton.innerHTML = 'Complete Order';
        } else {
            if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                document.getElementById('id_payment_intent_id').value = result.paymentIntent.id;
                form.submit();
            }
        }
    });
});
