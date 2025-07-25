import logging
import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string

from bag.context_processors import bag_contents
from profiles.models import UserProfile

from .forms import CheckoutForm, ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

logger = logging.getLogger(__name__)


def checkout(request):
    """
    View to handle the checkout process:
      - On GET: create a Stripe PaymentIntent, embed its secret in the page
      - On POST: verify that payment succeeded and then create the Order
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    # Always define these so they exist no matter which branch we hit:
    client_secret = None
    payment_intent_id = None

    # 1) Pull bag contents and compute total
    bag = bag_contents(request)
    bag_items = bag["bag_items"]
    subtotal = bag["total"]
    delivery_cost = bag["delivery"]
    free_delivery_delta = bag["free_delivery_delta"]
    final_total = bag["grand_total"]

    if subtotal == 0:
        messages.warning(
            request,
            "Your cart is empty. Please add items to proceed to checkout."
        )
        return redirect("view_bag")

    # 2) Use the total including delivery for Stripe
    stripe_total = round(final_total * 100)  # amount in cents

    if request.method == "POST":
        # ───────────────────────────────────────────────
        # A) PROCESS A FORM SUBMISSION (after Stripe confirmed payment)
        # ───────────────────────────────────────────────
        form = CheckoutForm(request.POST, user=request.user)

        # Debugging: Print form errors if validation fails
        if not form.is_valid():
            print("Form validation failed:")
            print(form.errors)

        # Retrieve the PaymentIntent ID from the hidden <input>
        payment_intent_id = request.POST.get("payment_intent_id")
        if not payment_intent_id:
            messages.error(
                request, "Payment information is missing. Please try again."
            )
            return redirect("checkout")

        # Verify with Stripe that the PaymentIntent succeeded
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            messages.error(request, f"Unable to verify payment: {str(e)}")
            return redirect("checkout")

        if intent.status != "succeeded":
            messages.error(
                request, "Payment was not successful. Please try again."
            )
            return redirect("checkout")

        # Process the form data if valid
        if form.is_valid():
            create_user_profile = form.cleaned_data.get(
                "create_user_profile", False
            )
            saved_address = form.cleaned_data.get("saved_address")

            user_profile = None

            if create_user_profile and not request.user.is_authenticated:
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                User = get_user_model()
                try:
                    # Try existing account
                    user = User.objects.get(username=email)
                except User.DoesNotExist:
                    # Otherwise create a new one
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                    )

                # Manually set the backend (so login() knows which to pick)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                # Ensure profile exists, error handling - don't double-create
                user_profile, _ = UserProfile.objects.get_or_create(user=user)

            elif request.user.is_authenticated:
                user_profile = request.user.userprofile

            # Handle gift message
            session_bag = request.session.get('bag', {})
            is_gift_val = False
            gift_message_val = None
            if 'gift' in session_bag:
                gift_info = session_bag['gift']
                is_gift_val = gift_info.get('is_gift', False)
                raw_msg = gift_info.get('gift_message', '').strip()
                gift_message_val = raw_msg if raw_msg else None

            # Handle shipping address
            store_shipping = form.cleaned_data.get(
                "store_shipping_address", False
            )
            saved_address = form.cleaned_data.get("saved_address")

            if request.user.is_authenticated and store_shipping:
                # User wants to save/update an address
                if saved_address:
                    # Overwrite the existing saved address
                    saved_address.full_name = form.cleaned_data["full_name"]
                    saved_address.phone_number = (
                        form.cleaned_data["phone_number"]
                    )
                    saved_address.street_address1 = (
                        form.cleaned_data["street_address1"]
                    )
                    saved_address.street_address2 = (
                        form.cleaned_data["street_address2"]
                    )
                    saved_address.town_or_city = (
                        form.cleaned_data["town_or_city"]
                    )
                    saved_address.county = form.cleaned_data["county"]
                    saved_address.eircode = form.cleaned_data["eircode"]
                    saved_address.country = form.cleaned_data["country"]
                    saved_address.save()
                    shipping_address = saved_address
                else:
                    # Create a brand-new shipping address on their profile
                    shipping_address = ShippingAddress.objects.create(
                        user_profile=request.user.userprofile,
                        full_name=form.cleaned_data["full_name"],
                        phone_number=form.cleaned_data["phone_number"],
                        street_address1=form.cleaned_data["street_address1"],
                        street_address2=form.cleaned_data["street_address2"],
                        town_or_city=form.cleaned_data["town_or_city"],
                        county=form.cleaned_data["county"],
                        eircode=form.cleaned_data["eircode"],
                        country=form.cleaned_data["country"],
                    )
            else:
                # Save it, not linked to profile) but attached to order
                shipping_address = ShippingAddress.objects.create(
                    full_name=form.cleaned_data["full_name"],
                    phone_number=form.cleaned_data["phone_number"],
                    street_address1=form.cleaned_data["street_address1"],
                    street_address2=form.cleaned_data["street_address2"],
                    town_or_city=form.cleaned_data["town_or_city"],
                    county=form.cleaned_data["county"],
                    eircode=form.cleaned_data["eircode"],
                    country=form.cleaned_data["country"],
                )

            # Create the Order
            order = Order.objects.create(
                user_profile=user_profile,
                shipping_address=shipping_address,
                email=form.cleaned_data['email'],
                total_price=final_total,
                stripe_pid=payment_intent_id,
                is_gift=is_gift_val,
                gift_message=gift_message_val,
            )

            for item in bag_items:
                product_obj = item['product']
                quantity = item['quantity']
                price_now = product_obj.price

                OrderItem.objects.create(
                    order=order,
                    product=product_obj,
                    quantity=quantity,
                    price_at_time=price_now,
                    is_gift=is_gift_val,
                    gift_message=gift_message_val,
                )
            order.update_total()

            # Clear the bag from session
            if "bag" in request.session:
                del request.session["bag"]

            # Debugging: Print success messages
            print("Form is valid. Proceeding to create order...")
            print("Redirecting to checkout_success...")

            # Redirect to success
            return redirect(
                "checkout_success", order_number=order.order_number
            )

    else:
        # ───────────────────────────────────────────────
        # B) PROCESS A GET REQUEST
        # ───────────────────────────────────────────────
        form = CheckoutForm(user=request.user)

    # Create a fresh PaymentIntent for GET or invalid POST
    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            payment_method_types=["card"],
        )
        client_secret = intent.client_secret
        payment_intent_id = intent.id
    except stripe.error.StripeError as e:
        messages.error(request, f"Error creating payment intent: {str(e)}")
        client_secret = None
        payment_intent_id = None

    # Warn if keys are missing or if the secret wasn’t created.
    if not stripe_public_key:
        messages.warning(
            request,
            (
                "Stripe public key is missing. "
                "Did you set it in your environment?"
            )
        )
    if request.method == "GET" and not client_secret:
        messages.warning(
            request,
            "Payment form could not be initialized. Please try again later."
        )

    context = {
        "form": form,
        "bag_items": bag_items,
        "subtotal": subtotal,
        "delivery_cost": delivery_cost,
        "free_delivery_delta": free_delivery_delta,
        "final_total": final_total,
        "settings": settings,
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret,
        "payment_intent_id": payment_intent_id,
    }

    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    # Retrieve the order using the order number
    order = get_object_or_404(Order, order_number=order_number)

    # Display a success message to the user
    messages.success(
        request,
        f'Payment successful, order is processed! '
        f'Your order number is {order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    # Clear the shopping bag from the session
    if 'bag' in request.session:
        del request.session['bag']

    # Pass the order to the template
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    subject = f"Order Confirmation - {order.order_number}"
    body = render_to_string(
        "checkout/order_confirmation_email.html",
        {"order": order}
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
            fail_silently=False,
        )
        logger.info(f"Confirmation email sent to {order.email}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {e}")
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
    address = get_object_or_404(
        ShippingAddress,
        id=address_id,
        user_profile=request.user.userprofile
    )
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipping address updated successfully.')
            return redirect('manage_addresses')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'checkout/edit_address.html', {'form': form})


@csrf_exempt
def stripe_webhook(request):
    """Endpoint for receiving Stripe webhooks."""
    # 1) Verify the signature
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = os.getenv("STRIPE_WH_SECRET", "")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=endpoint_secret,
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error("❌ Webhook verification failed: %s", e)
        return HttpResponse(status=400)

    # 2) Handle the event
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        pid = intent["id"]

        try:
            order = Order.objects.get(stripe_pid=pid)
        except Order.DoesNotExist:
            logger.error("Order with pid %s not found!", pid)
            return HttpResponse(status=200)

        # Mark order as paid
        order.status = "paid"
        order.stripe_pid = pid
        order.save(update_fields=["status", "stripe_pid"])
        logger.info("Order %s marked as paid.", order.order_number)

    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        pid = intent["id"]
        logger.warning("PaymentIntent failed: %s", pid)

    else:
        # Any other event types you want to handle
        logger.debug("Unhandled event type %s", event["type"])

    # 3) Return a 200 so Stripe knows we received it
    return HttpResponse(status=200)
