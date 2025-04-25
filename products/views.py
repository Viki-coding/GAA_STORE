from django.shortcuts import renderget_object_or_404
from .models import Product, Hurley, Grip, Sliotar, Helmet

# Create your views here.
def product_list(request):
    """
    View to display a list of all products.
    """
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