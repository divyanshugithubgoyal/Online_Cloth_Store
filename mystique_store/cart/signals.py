from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem

@receiver(post_save, sender=CartItem)
def cart_item_saved(sender, instance, **kwargs):
    """Log when cart item is saved"""
    print(f"Cart item saved: {instance.product.name} x{instance.quantity}")

@receiver(post_delete, sender=CartItem)
def cart_item_deleted(sender, instance, **kwargs):
    """Log when cart item is deleted"""
    print(f"Cart item deleted: {instance.product.name}")