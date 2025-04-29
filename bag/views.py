from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Hurley, Grip, Sliotar, Helmet


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


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

    # Retrieve the bag from the session (or initialize it if it doesn't exist)
    bag = request.session.get('bag', {})

    # Check if the product is already in the bag and update the quantity
    if product_id in list(bag.keys()):
        bag[product_id] += quantity
    else:
        bag[product_id] = quantity

    # Save the updated bag back to the session
    request.session['bag'] = bag

    # Add a success message
    messages.success(request, f'Added {quantity} x {product.name} to your bag.')

    # Redirect to the specified URL
    return redirect(request.POST.get('redirect_url'))