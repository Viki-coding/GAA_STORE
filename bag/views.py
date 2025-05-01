from django.shortcuts import render

def view_bag(request):
    """
    View to display the shopping bag.
    """
    bag = request.session.get('bag', {})  # Retrieve the bag from the session
    return render(request, 'bag/bag.html', {'bag': bag})

    
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

    # Create a unique key for the product based on its attributes
    if isinstance(specific_product, Hurley):
        size = request.POST.get('size')
        weight = request.POST.get('weight')
        grip_color = request.POST.get('grip_color')
        manufacturer = specific_product.manufacturer.name
        product_key = f"{product_id}-{size}-{weight}-{grip_color}-{manufacturer}"
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({
            'product_id': product_id,
            'size': size,
            'weight': weight,
            'grip_color': grip_color,
            'manufacturer': manufacturer,
        })
    elif isinstance(specific_product, Grip):
        color = specific_product.color
        product_key = f"{product_id}-{color}"
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({
            'product_id': product_id,
            'color': color,
        })
    elif isinstance(specific_product, Sliotar):
        color = specific_product.color
        product_key = f"{product_id}-{color}"
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({
            'product_id': product_id,
            'color': color,
        })
    elif isinstance(specific_product, Helmet):
        size = specific_product.size
        color = specific_product.color
        product_key = f"{product_id}-{size}-{color}"
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({
            'product_id': product_id,
            'size': size,
            'color': color,
        })
    else:
        # Default case for products without specific attributes
        product_key = str(product_id)
        bag[product_key] = bag.get(product_key, {'quantity': 0})
        bag[product_key]['quantity'] += quantity
        bag[product_key].update({
            'product_id': product_id,
        })

    # Save the updated bag back to the session
    request.session['bag'] = bag

    # Add a success message
    messages.success(request, f'Added {quantity} x {product.name} to your bag.')

    # Redirect to the specified URL
    return redirect(request.POST.get('redirect_url'))