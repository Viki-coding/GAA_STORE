from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Hurley, Grip, Sliotar, Helmet


# Create your views here.
def product_list(request):
    """
    View to display a list of all products or filter by category.
    """
    products = Product.objects.all()  # Fetch all products
    return render(request, 'products/product_list.html', {'products': products})
    # category = request.GET.get('category')
    # if category:
    #     products = Product.objects.filter(description__icontains=category)
    # else:
    #     products = Product.objects.all()
    # return render(
    #     request, 'products/product_list.html', {'products': products})


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
    manufacturer_choices = Hurley._meta.get_field('manufacturer').choices   

    return render(request, 'products/hurley_detail.html', {
        'hurley': hurley,
        'size_choices': size_choices,
        'weight_choices': weight_choices,
        'grip_color_choices': grip_color_choices,
        'manufacturer_choices': manufacturer_choices,
    })


def add_to_bag(request, product_id):
    """
    Add a hurley to the shopping bag.
    """
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    weight = request.POST.get('weight')
    grip_color = request.POST.get('grip_color')
    manufacturer = request.POST.get('manufacturer')
    quantity = int(request.POST.get('quantity', 1))

    bag = request.session.get('bag', {})

    # Create a unique key for the hurley based on its attributes,
    # prevents overwriting
    # hurleys with the same product ID but different attributes
    hurley_key = f"{product_id}-{size}-{weight}-{grip_color}-{manufacturer}"

    if hurley_key in bag:
        bag[hurley_key]['quantity'] += quantity
    else:
        bag[hurley_key] = {
            'product_id': product_id,
            'size': size,
            'weight': weight,
            'grip_color': grip_color,
            'manufacturer': manufacturer,
            'quantity': quantity,
        }
    
    request.session['bag'] = bag
    return redirect('hurley_detail', hurley_id=product_id)

