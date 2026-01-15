from .models import Order, OrderItem
from cart.utils import get_cart_items, get_cart_total

def create_order_from_cart(request):
    """Create order from cart items"""
    if not request.user.is_authenticated:
        return None
    
    cart_items = get_cart_items(request)
    if not cart_items:
        return None
    
    # Get shipping details from POST data
    full_name = request.POST.get('full_name', request.user.get_full_name())
    email = request.POST.get('email', request.user.email)
    phone = request.POST.get('phone', '')
    address = request.POST.get('address', '')
    city = request.POST.get('city', '')
    zip_code = request.POST.get('zip_code', '')
    
    total = get_cart_total(request)
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        city=city,
        zip_code=zip_code,
        total_amount=total
    )
    
    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price
        )
    
    return order
