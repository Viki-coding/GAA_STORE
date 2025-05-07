from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from products.models import Product, Hurley, Grip, Sliotar, Helmet


def view_bag(request):
    """
    View to display the shopping bag.
    """
    bag = request.session.get('bag', {})  # Retrieve the bag from the session
    bag_items = []
    bag_total = 0  # Initialize the total cost of items in the bag

    for product_key, item in bag.items():
        product_id = item['product_id']  # Use the actual product ID
        try:
            product = Product.objects.get(id=product_id)  # Fetch the product
        except Product.DoesNotExist:
            # Handle the case where the product no longer exists
            continue
        total_price = product.price * item['quantity']  # Calculate total price
        bag_items.append({
            'product': product,
            'quantity': item['quantity'],
            'total_price': total_price,
            'attributes': {
                key: value for key, value in item.items() if key not in [
                    'product_id', 'quantity']}
        })
        bag_total += total_price  # Add to the bag total

    # Calculate delivery costs and grand total
    delivery = 0
    free_delivery_delta = 0
    grand_total = bag_total

    if bag_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = bag_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - bag_total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = bag_total + delivery

    return render(request, 'bag/bag.html', {
        'bag_items': bag_items,
        'bag_total': bag_total,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    })


def add_to_bag(request, product_id):
    """ Add a quantity of the specified product to the shopping bag """

    # Get the quantity and redirect URL from the POST request
    try:
        quantity = int(request.POST.get('quantity'))
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity. Please try again.")
        return redirect(request.POST.get('redirect_url'))

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
        product_key = f"{product_id}-{size}-{weight}-{grip_color}-{manufacturer}"
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


def update_bag(request, product_id):
    """Update the quantity of a specific product in the shopping bag."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        bag = request.session.get('bag', {})

        # Find the product in the bag and update its quantity
        for product_key, item in bag.items():
            if item['product_id'] == product_id:
                if quantity > 0:
                    item['quantity'] = quantity
                    messages.success(request, f"Updated {item['quantity']} x {item['product_id']} in your bag.")
                else:
                    del bag[product_key]
                    messages.success(request, "Removed item from your bag.")
                break

        request.session['bag'] = bag  # Save the updated bag to the session
        return redirect('view_bag')