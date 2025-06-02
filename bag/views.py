from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from products.models import Product, Hurley, Grip, Sliotar, Helmet
from django.http import JsonResponse


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """

    # Get the quantity and redirect URL from the POST request
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
    except (ValueError, TypeError):
        error_msg = (
            "Invalid quantity. Please enter a valid number greater than zero."
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(
                {'success': False, 'message': error_msg},
                status=400
            )
        messages.error(request, error_msg)
        redirect_url = request.POST.get(
            'redirect_url', request.META.get('HTTP_REFERER', '/')
        )
        return redirect(redirect_url)

    # Validate the product ID
    product = get_object_or_404(Product, id=product_id)

    # Determine the specific product type (Hurley, Grip, Sliotar, Helmet)
    specific_product = product.get_specific_instance()

    # Retrieve the bag from the session (or initialize it if it doesn't exist)
    bag = request.session.get('bag', {})

    # Helper function to update the bag
    def update_bag(bag, product_key, product_id, quantity, **attributes):
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({'product_id': product_id, **attributes})

    # Create a unique key for the product based on its attributes
    if isinstance(specific_product, Hurley):
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        grip_color = request.POST.get('grip_color')
        manufacturer = specific_product.manufacturer.name
        size = size if size is not None else "unknown"
        weight = weight if weight is not None else "unknown"
        grip_color = grip_color if grip_color is not None else "unknown"
        manufacturer = manufacturer if manufacturer is not None else "unknown"
        product_key = f"{
            product_id}-{size}-{weight}-{grip_color}-{manufacturer}"
        update_bag(
            bag, product_key, product_id, quantity,
            size=size,
            weight=weight,
            grip_color=grip_color,
            manufacturer=manufacturer,
        )
    elif isinstance(specific_product, Grip):
        color = specific_product.color
        product_key = f"{product_id}-{color}"
        update_bag(bag, product_key, product_id, quantity, color=color)
    elif isinstance(specific_product, Sliotar):
        color = specific_product.color
        product_key = f"{product_id}-{color}"
        update_bag(bag, product_key, product_id, quantity, color=color)
    elif isinstance(specific_product, Helmet):
        size = specific_product.size
        color = specific_product.color
        product_key = f"{product_id}-{size}-{color}"
        update_bag(
            bag, product_key, product_id, quantity, size=size, color=color)
    else:
        # Default case for products without specific attributes
        product_key = str(product_id)
        update_bag(bag, product_key, product_id, quantity)

    # Save the updated bag back to the session
    request.session['bag'] = bag

    # Handle AJAX requests
    success_msg = f'Added {quantity} x {product.name} to your bag.'
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': success_msg,
            'bag_count': sum(item['quantity'] for item in bag.values())
        })

    # Handle non-AJAX requests
    messages.success(request, success_msg)
    redirect_url = request.POST.get(
        'redirect_url', request.META.get('HTTP_REFERER', '/')
    )
    return redirect(redirect_url)

    # Add a success message
    messages.success(
        request, f'Added {quantity} x {product.name} to your bag.')

    # Validate and redirect to the specified URL
    redirect_url = request.POST.get('redirect_url')
    try:
        redirect_url = resolve_url(redirect_url)
    except Exception:
        redirect_url = '/'

    # Return the redirect response
    return redirect(redirect_url)


def update_bag(request, product_key):
    """Update the quantity of a specific product in the shopping bag."""
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
        except (ValueError, TypeError):
            error_msg = "Invalid quantity. Please try again."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {'success': False, 'message': error_msg},
                    status=400
                )
            messages.error(request, error_msg)
            return redirect('view_bag')

        bag = request.session.get('bag', {})

        # Update the quantity or remove the item if quantity is 0
        if product_key in bag:
            if quantity > 0:
                bag[product_key]['quantity'] = quantity
                msg = (
                    f"Updated {bag[product_key]['quantity']} x "
                    f"{bag[product_key]['product_id']} in your bag."
                )
            else:
                del bag[product_key]
                msg = "Removed item from your bag."
        else:
            msg = "Item not found in your bag."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {'success': False, 'message': msg},
                    status=404
                )
            messages.error(request, msg)
            return redirect('view_bag')
        request.session['bag'] = bag

        # AJAX response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': msg})

        # Non-AJAX response
        messages.success(request, msg)
        return redirect('view_bag')


def remove_from_bag(request, product_key):
    """Remove a specific product from the shopping bag."""
    bag = request.session.get('bag', {})

    if product_key in bag:
        del bag[product_key]
        msg = "Removed item from your bag."
        success = True
    else:
        msg = "Item not found in your bag."
        success = False

    # Save the updated bag back to the session
    request.session['bag'] = bag
    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        status = 200 if success else 404
        return JsonResponse(
            {'success': success, 'message': msg},
            status=status
        )

    # Non-AJAX response
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, msg)
    return redirect('view_bag')


def add_gift_message(request):
    """Add a gift message to the shopping bag."""
    if request.method == 'POST':
        is_gift = request.POST.get('is_gift', False)
        gift_message = request.POST.get('gift_message', '')

        # Retrieve the bag from the session
        bag = request.session.get('bag', {})

        # Add gift message to the session
        bag['gift'] = {
            'is_gift': bool(is_gift),
            'gift_message': gift_message,
        }

    # Save the updated bag back to the session
    request.session['bag'] = bag
    messages.success(request, "Gift message added to your bag.")
    return redirect('view_bag')
