from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, ShippingAddress
from profiles.models import UserProfile
from bag.context_processors import bag_contents
from .forms import CheckoutForm
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    """
    View to handle the checkout process.
    """
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
        )

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_number=order.order_number)

    # Get the bag contents and pass them to the template, initialize form.
  
    form = CheckoutForm()
    bag = bag_contents(request)
    bag_items = bag['bag_items']
    grand_total = bag['grand_total']

    context = {
        'form': form,
        'bag_items': bag_items,
        'grand_total': grand_total,
    }

    return render(request, 'checkout/checkout.html', context)




def process_payment(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        try:
            # Create a PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=5000,  # Amount in cents (e.g., $50.00)
                currency='usd',
                payment_method=payment_method_id,
                confirm=True,
            )
            return redirect('payment_success')
        except stripe.error.CardError as e:
            return render(request, 'checkout.html', {'error': str(e)})