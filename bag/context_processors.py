from decimal import Decimal
from django.conf import settings
from products.models import Product


def bag_contents(request):
    """
    Makes the bag contents and delivery calculations
    available across all templates.
    """
    bag_items = []
    total = 0
    product_count = 0

    bag = request.session.get('bag', {})
    for product_key, item in bag.items():
        product_id = item.get('product_id')
        if not product_id:
            continue
        quantity = item.get('quantity', 1)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        # Calculate total price for the item
        total_price = product.price * quantity
        bag_items.append({
            'product_key': product_key,
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
            'size': item.get('size'),
            'color': item.get('color'),
            'manufacturer': item.get('manufacturer'),
        })

        # Update totals
        total += total_price
        product_count += quantity

    # Calculate delivery costs
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }


def bag_count(request):
    bag = request.session.get('bag', {})
    count = sum(item.get('quantity', 0) for item in bag.values())
    return {'bag_count': count}
