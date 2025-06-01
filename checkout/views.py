import uuid
import stripe

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from .models import Order, ShippingAddress
from profiles.models import UserProfile
from bag.context_processors import bag_contents
from .forms import CheckoutForm
from .forms import ShippingAddressForm


def checkout(request):
    """
    View to handle the checkout process and create stripe payment intent.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    create_user_profile = False
    store_shipping_address = False

    # Get the current bag contents and calculate the total
    bag = bag_contents(request)
    bag_items = bag['bag_items']
    grand_total = bag['grand_total']

    # Redirect if the cart is empty
    if grand_total == 0:
        messages.warning(
            request, (
                "Your cart is empty. Please add items to proceed to checkout."
            ))
        return redirect('view_bag')
    
    stripe_total = round(grand_total * 100)  # Convert to cents for Stripe

    # Collect form data and create a payment intent
    if request.method == 'POST':
        # Get form data
        form = CheckoutForm(request.POST or None, user=request.user)
        if form.is_valid():
            # Extract cleaned data from the form
            create_user_profile = form.cleaned_data.get('create_user_profile', False)
            store_shipping_address = form.cleaned_data.get('store_shipping_address', False)
            saved_address = form.cleaned_data.get('saved_address')

            # Process user profile creation
            user_profile = None
            if create_user_profile and not request.user.is_authenticated:
                # Create a new user and profile
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')  # Add this field to your form
                password2 = form.cleaned_data.get('password2')

                # Validate passwords match
                if password != password2:
                    messages.error(request, "Passwords do not match.")
                    return redirect('checkout')

                # Create user (using email as username)
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                user_profile = UserProfile.objects.create(user=user)
                login(request, user)  # Log the user in

            elif request.user.is_authenticated:
                # Use existing profile
                user_profile = request.user.userprofile

            # Process shipping address
            if store_shipping_address and user_profile:
                # Save the address from the form data
                ShippingAddress.objects.create(
                    user_profile=user_profile,
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone_number=form.cleaned_data['phone_number'],
                    street_address1=form.cleaned_data['street_address1'],
                    street_address2=form.cleaned_data['street_address2'],
                    town_or_city=form.cleaned_data['town_or_city'],
                    county=form.cleaned_data['county'],
                    eircode=form.cleaned_data['eircode'],
                    country=form.cleaned_data['country']
                )

    # if request.method == 'POST':
    #     create_user_profile = request.POST.get('create_user_profile') == 'on'
    #     store_shipping_address = request.POST.get('store_shipping_address') == 'on'
    #     form = CheckoutForm(request.POST, user=request.user)
    #     if form.is_valid():
    #         # Check if the user selected a saved address
    #         saved_address = form.cleaned_data.get('saved_address')
    #         create_user_profile = form.cleaned_data.get('create_user_profile', False)
    #         # Create user profile if requested
    #         if create_profile and not request.user.is_authenticated:
    #             user = User.objects.create_user(
    #                 username=email,  # Use email as username or generate a unique username
    #                 email=email,
    #                 password=request.POST.get('password')  # Add a password field to your form
    #                 )
    #             user_profile = UserProfile.objects.create(user=user)
    #             # Log the user in
    #             login(request, user)
    #         elif request.user.is_authenticated:
    #             user_profile = request.user.userprofile
            
    #                     # Save shipping address if requested
    #         if save_address and user_profile:
    #             ShippingAddress.objects.create(
    #                 user_profile=user_profile,
    #                 full_name=full_name,
    #                 phone_number=phone_number,
    #                 street_address1=street_address1,
    #                 street_address2=street_address2,
    #                 town_or_city=town_or_city,
    #                 county=county,
    #                 eircode=eircode,
    #                 country=country

            else:
                # Use the new address entered in the form
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone_number = request.POST.get('phone_number')
                street_address1 = request.POST.get('street_address1')
                street_address2 = request.POST.get('street_address2')
                town_or_city = request.POST.get('town_or_city')
                county = request.POST.get('county')
                eircode = request.POST.get('eircode')
                store_shipping_address = request.POST.get(
                    'store_shipping_address') == 'on'
                create_user_profile = request.POST.get('create_user_profile') == 'on'

        # Get the current bag contents and calculate the total
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Convert to cents for Stripe

        try:
            # Create a PaymentIntent with the order amount
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                payment_method_types=['card'],
            )
            client_secret = intent.client_secret

        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
        except stripe.error.CardError as e:
            # Handle card errors (declined, etc.)
            messages.error(request, f"Card error: {e.user_message}")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, f"Invalid request: {str(e)}")
        except stripe.error.StripeError as e:
            # Generic Stripe error
            messages.error(request, f"Stripe error: {str(e)}")
        except Exception as e:
            # Something else happened
            messages.error(request, f"Serious error: {str(e)}")


        # Create or retrieve user profile
        user_profile = None
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
        elif create_user_profile:
            # Create a new user profile (if not logged in)
            user_profile = UserProfile.objects.create(
                user=request.user,
                default_phone_number=phone_number,
                default_street_address1=street_address1,
                default_street_address2=street_address2,
                default_town_or_city=town_or_city,
                default_county=county,
                default_eircode=eircode,
            )

        # Save shipping address if requested
        shipping_address = None
        if store_shipping_address and user_profile:
            shipping_address = ShippingAddress.objects.create(
                user_profile=user_profile,
                full_name=full_name,
                phone_number=phone_number,
                street_address1=street_address1,
                street_address2=street_address2,
                town_or_city=town_or_city,
                county=county,
                eircode=eircode,
            )

        # Create the order
        order = Order.objects.create(
            user_profile=None,
            shipping_address=shipping_address,
            total_price=bag_contents(request)['grand_total'],
            stripe_pid=intent.id,
        )

        # Redirect to the order confirmation page
        return redirect('checkout_success', order_number=order.order_number)

        # Handle AJAX and regular form submissions
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return JSON response for AJAX requests
            return JsonResponse({
                'client_secret': intent.client_secret,
                'order_id': order.id,
            })
        else:
            # Redirect for regular form submissions
            messages.success(
                request, 'Your order has been placed successfully!')
            return redirect(
                'order_confirmation', order_number=order.order_number)

    else:
        # For GET requests, create a PaymentIntent
        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
                payment_method_types=['card'],
            )
            client_secret = intent.client_secret
        except Exception as e:
            messages.error(request, f'Error creating payment intent: {str(e)}')
            client_secret = None

    # Check for missing keys
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    if not client_secret:
        messages.warning(
            request, 'Stripe client secret could not be generated. \
            Please try again later.')

    # Handle GET request
    form = CheckoutForm()

    context = {
        'form': form,
        'bag_items': bag_items,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # Retrieve the order using the order number
    order = get_object_or_404(Order, order_number=order_number)

    # Display a success message to the user
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Clear the shopping bag from the session
    if 'bag' in request.session:
        del request.session['bag']

    # Pass the order to the template
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)

@login_required
def add_address(request):
    """
    View to add a new shipping address.
    """
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_profile = request.user.userprofile
            address.save()
            messages.success(request, 'Shipping address added successfully.')
            return redirect('manage_addresses')
    else:
        form = ShippingAddressForm()
    return render(request, 'checkout/add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    """
    View to edit an existing shipping address.
    """
    address = get_object_or_404(ShippingAddress, id=address_id, user_profile=request.user.userprofile)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipping address updated successfully.')
            return redirect('manage_addresses')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'checkout/edit_address.html', {'form': form})

