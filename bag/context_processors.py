from decimal import Decimal
from django.conf import settings
from products.models import Product

def bag_contents(request):
    """
    Makes the bag contents and delivery calculations available across all templates.
    """
    bag_items = []
    total = 0
    product_count = 0

    bag = request.session.get('bag', {})
    for product_id, quantity in bag.items():
        product = Product.objects.get(id=product_id)
        total_price = product.price * quantity
        bag_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
        total += total_price
        product_count += quantity

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