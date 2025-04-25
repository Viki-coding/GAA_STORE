from django.shortcuts import render, get_object_or_404
from .models import Product, Hurley, Grip, Sliotar, Helmet

# Create your views here.
def product_list(request):
    """
    View to display a list of all products or filter by category.
    """
    category = request.GET.get('category')  
    if category:
        products = Product.objects.filter(description__icontains=category)
    else:
        products = Product.objects.all()
    return render(
        request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    """
    View to display the details of a specific product.
    """
    product = get_object_or_404(Product, id=product_id)
    specific_product = product.get_specific_instance()
    return render(request, 'products/product_detail.html', {
        'product': specific_product
    })


def hurleys_shop(request):
    """
    View to display the Hurley shop page. This will show the categories of 
    hurleys, Bambú, Ash and Goalie.  
    """
    return render(request, 'products/hurleys_shop.html', {})