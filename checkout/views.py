from django.shortcuts import render


def checkout(request):
    """
    View to handle the checkout process.
    """
    return render(request, 'checkout/checkout.html')
