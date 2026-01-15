# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .utils import (
    add_to_cart, remove_from_cart, update_cart_quantity,
    get_cart_items, get_cart_total, clear_cart
)
from .models import Coupon
from decimal import Decimal

def cart_view(request):
    """Display cart page"""
    items = get_cart_items(request)
    total = get_cart_total(request)
    
    context = {
        'cart_items': items,
        'cart_total': total,
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart_view(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    add_to_cart(request, product_id, quantity)
    messages.success(request, f'{product.name} added to cart!')
    
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))

def remove_from_cart_view(request, product_id):
    """Remove product from cart"""
    remove_from_cart(request, product_id)
    messages.info(request, 'Product removed from cart')
    return redirect('cart:cart')

def update_cart_view(request, product_id):
    """Update product quantity in cart"""
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        update_cart_quantity(request, product_id, quantity)
        messages.success(request, 'Cart updated')
    return redirect('cart:cart')

def clear_cart_view(request):
    """Clear all items from cart"""
    clear_cart(request)
    messages.info(request, 'Cart cleared')
    return redirect('cart:cart')

def checkout_view(request):
    """Checkout page"""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to checkout')
        return redirect('authentication:login')
    
    items = get_cart_items(request)
    if not items:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart:cart')
    
    total = get_cart_total(request)
    
    if request.method == 'POST':
        # Process checkout
        from orders.utils import create_order_from_cart
        order = create_order_from_cart(request)
        
        if order:
            clear_cart(request)
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'cart_items': items,
        'cart_total': total,
    }
    return render(request, 'cart/checkout.html', context)

def apply_coupon_view(request):
    """Apply coupon code"""
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip()
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            request.session['coupon_code'] = code
            messages.success(request, 'Coupon Added!')
            return redirect('cart:cart')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')
            return redirect('cart:cart')
    return redirect('cart:cart')