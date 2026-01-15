from .utils import get_cart_count, get_cart_total

def cart_context(request):
    """Add cart information to all templates"""
    return {
        'cart_count': get_cart_count(request),
        'cart_total': get_cart_total(request),
    }