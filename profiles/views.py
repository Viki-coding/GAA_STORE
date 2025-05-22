from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import ShippingAddress
from checkout.forms import ShippingAddressForm


def profile(request):
    """ Display the user's profile. """

    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)


@login_required
def manage_addresses(request):
    """
    View to display and manage saved shipping addresses.
    """
    addresses = ShippingAddress.objects.filter(
        user_profile=request.user.userprofile)
    return render(
        request, 'profiles/manage_addresses.html', {'addresses': addresses})


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
            return redirect('manage_addresses')
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
    return redirect('manage_addresses')
