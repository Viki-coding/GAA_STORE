from allauth.account.forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import ShippingAddress, Order
from checkout.forms import ShippingAddressForm


# def login_signup_view(request):
#     if request.user.is_authenticated:
#         return redirect('profile')
 
#     login_form = AuthenticationForm()
#     signup_form = SignupForm()
#     return render(request, 'profiles/login.html', {
#         'form': login_form,
#         'signup_form': signup_form,
#     })


@login_required
def profile(request):
    """ Display the user's profile with shipping addresses and orders. """
    addresses = ShippingAddress.objects.filter(user_profile=request.user.userprofile)
    orders = Order.objects.filter(user_profile=request.user.userprofile)  # Assuming an Order model exists

    # Initialize Allauth's SignupForm
    signup_form = SignupForm()

    template = 'profiles/profile.html'
    context = {
        'addresses': addresses,
        'orders': orders,
        'signup_form': signup_form,
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
            # Redirect back to the profile page (where addresses are listed)
            return redirect('profile')
    else:
        form = ShippingAddressForm()
    return render(request, 'profiles/add_address.html', {'form': form})


@login_required
def edit_address(request, address_id):
    """
    View to edit an existing shipping address.
    """
    address = get_object_or_404(
        ShippingAddress, id=address_id, user_profile=request.user.userprofile)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipping address updated successfully.')
            return redirect('profile')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, 'profiles/edit_address.html', {'form': form})


@login_required
def delete_address(request, address_id):
    """
    View to delete a shipping address.
    """
    address = get_object_or_404(
        ShippingAddress, id=address_id, user_profile=request.user.userprofile)
    address.delete()
    messages.success(request, 'Shipping address deleted successfully.')
    return redirect('profile')


@login_required
def order_detail(request, order_id):
    """
    Display detailed information about a specific order.
    """
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.userprofile)

    template = 'checkout/order_detail.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
