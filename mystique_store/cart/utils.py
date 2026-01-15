from decimal import Decimal
from .models import Cart, CartItem
from products.models import Product

class SessionCart:
    """Session-based cart for anonymous users"""
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, product_id, quantity=1):
        """Add product to session cart"""
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity}
        self.save()
    
    def remove(self, product_id):
        """Remove product from session cart"""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def update_quantity(self, product_id, quantity):
        """Update product quantity"""
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()
    
    def clear(self):
        """Clear the cart"""
        del self.session['cart']
        self.save()
    
    def save(self):
        """Save cart to session"""
        self.session.modified = True
    
    def get_items(self):
        """Get all cart items with product details"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        for product in products:
            quantity = self.cart[str(product.id)]['quantity']
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
        return items
    
    def get_total(self):
        """Calculate total price"""
        return sum(Decimal(item['subtotal']) for item in self.get_items())
    
    def get_items_count(self):
        """Get total number of items"""
        return sum(item['quantity'] for item in self.cart.values())

def get_user_cart(user):
    """Get or create cart for authenticated user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def add_to_cart(request, product_id, quantity=1):
    """Add product to cart (user or session based)"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        session_cart = SessionCart(request)
        session_cart.add(product_id, quantity)

def remove_from_cart(request, product_id):
    """Remove product from cart"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    else:
        session_cart = SessionCart(request)
        session_cart.remove(product_id)

def update_cart_quantity(request, product_id, quantity):
    """Update product quantity in cart"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
    else:
        session_cart = SessionCart(request)
        session_cart.update_quantity(product_id, quantity)

def get_cart_items(request):
    """Get cart items for current user/session"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        return [{
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': item.get_subtotal()
        } for item in cart.items.all()]
    else:
        session_cart = SessionCart(request)
        return session_cart.get_items()

def get_cart_total(request):
    """Get total cart price"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        return cart.get_total()
    else:
        session_cart = SessionCart(request)
        return session_cart.get_total()

def get_cart_count(request):
    """Get total number of items in cart"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        return cart.get_items_count()
    else:
        session_cart = SessionCart(request)
        return session_cart.get_items_count()

def merge_session_cart_to_user(request, user):
    """Merge session cart into user cart after login/registration"""
    session_cart = SessionCart(request)
    if session_cart.cart:
        cart = get_user_cart(user)
        for product_id, data in session_cart.cart.items():
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': data['quantity']}
            )
            if not created:
                cart_item.quantity += data['quantity']
                cart_item.save()
        session_cart.clear()

def clear_cart(request):
    """Clear cart"""
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        cart.items.all().delete()
    else:
        session_cart = SessionCart(request)
        session_cart.clear()