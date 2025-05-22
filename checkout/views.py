from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, ShippingAddress
from profiles.models import UserProfile
from bag.context_processors import bag_contents
from .forms import CheckoutForm
import stripe
from django.conf import settings
from django.http import JsonResponse


def checkout(request):
    """
    View to handle the checkout process and create stripe payment intent.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if request.method == 'POST':
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
        except stripe.error.StripeError as e:
            messages.error(request, f"Stripe error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

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
            user_profile=user_profile,
            shipping_address=shipping_address,
            total_price=bag_contents(request)['grand_total'],
            stripe_pid=intent.id,
        )

        # Redirect to payment page with client_secret
        return JsonResponse({
            'client_secret': intent.client_secret,
            'order_id': order.id,
        })

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_number=order.order_number)

    # Get the bag contents and pass them to the template, initialize form.

    form = CheckoutForm()
    bag = bag_contents(request)
    bag_items = bag['bag_items']
    grand_total = bag['grand_total']

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    context = {
        'form': form,
        'bag_items': bag_items,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
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
