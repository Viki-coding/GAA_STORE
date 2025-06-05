from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Hurley, Grip, Sliotar, Helmet, Manufacturer


# Create your views here.
def product_list(request):
    """
    View to display a list of all products or filter by category.
    """
    products = Product.objects.all()  # Fetch all products
    return render(
        request,
        'products/product_list.html',
        {'products': products}
    )


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
    View to display the Hurley shop page. This will show the types of
    hurleys, Bambú, Ash and Goalie. if not type specified, show all hurleys.
    """
    hurley_type = request.GET.get('type')
    if hurley_type:
        hurleys = Hurley.objects.filter(
            product__description__icontains=hurley_type)
    else:
        hurleys = Hurley.objects.all()

    return render(request, 'products/hurleys_shop.html', {'hurleys': hurleys})


def accessories_shop(request):
    """
    View to display the accessories shop page. This will show the categories of
    grips, helmets and sliotars.
    """
    grips = Grip.objects.all()
    sliotars = Sliotar.objects.all()
    helmets = Helmet.objects.all()
    return render(request, 'products/accessories_shop.html', {
        'grips': grips,
        'sliotars': sliotars,
        'helmets': helmets,
    })


def hurley_detail(request, hurley_id):
    """
    View to display the details of a specific hurley.
    """
    hurley = get_object_or_404(Hurley, product_id=hurley_id)
    size_choices = Hurley._meta.get_field('size').choices
    weight_choices = Hurley._meta.get_field('weight').choices
    grip_color_choices = Hurley._meta.get_field('grip_color').choices
    manufacturers = Manufacturer.objects.all()

    # Filter manufacturers based on hurley type
    if hurley.type == 'ash':
        manufacturers = Manufacturer.objects.exclude(
            name='Torpey Bambú Hurley')
    elif hurley.type == 'bambu':
        manufacturers = Manufacturer.objects.filter(name='Torpey Bambú Hurley')
    else:
        manufacturers = Manufacturer.objects.all()

    return render(request, 'products/product_detail.html', {
        'product': hurley.product,
        'size_choices': size_choices,
        'weight_choices': weight_choices,
        'grip_color_choices': grip_color_choices,
        'manufacturers': manufacturers,
    })


def helmet_detail(request, helmet_id):
    helmet = get_object_or_404(Helmet, product_id=helmet_id)
    return render(request, 'products/product_detail.html', {
        'product': helmet.product,
        'size_choices': Helmet._meta.get_field('size').choices,
        'color_choices': Helmet._meta.get_field('color').choices,
    })


def grip_detail(request, grip_id):
    grip = get_object_or_404(Grip, product_id=grip_id)
    return render(request, 'products/product_detail.html', {
        'product': grip.product,
        'color_choices': Grip._meta.get_field('color').choices,
    })


def sliotar_detail(request, sliotar_id):
    sliotar = get_object_or_404(Sliotar, product_id=sliotar_id)
    return render(request, 'products/product_detail.html', {
        'product': sliotar.product,
        'color_choices': Sliotar._meta.get_field('color').choices,
    })
