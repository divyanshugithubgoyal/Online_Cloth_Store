from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Product, Category

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    """Ensure slug is created before saving product"""
    if not instance.slug:
        instance.slug = slugify(instance.name)
        # Make slug unique
        original_slug = instance.slug
        counter = 1
        while Product.objects.filter(slug=instance.slug).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, **kwargs):
    """Ensure slug is created before saving category"""
    if not instance.slug:
        instance.slug = slugify(instance.name)
