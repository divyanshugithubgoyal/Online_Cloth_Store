# from django.db import models

# Create your models here.

from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('ALL', 'All'),
        ('KIDS_FEMALE', 'Girls'),
        ('KIDS_MALE', 'Boys'),
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('FOOTWEAR', 'Footwear'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Product(models.Model):
    STOCK_STATUS = [
        ('IN_STOCK', 'In Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
    ]
    
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2XL'),
        ('FREE', 'Free Size'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/')
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS, default='IN_STOCK')
    available_sizes = models.CharField(max_length=200, help_text='Comma-separated sizes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        return self.stock_status == 'IN_STOCK'
    
    def get_sizes_list(self):
        if self.available_sizes:
            return [s.strip() for s in self.available_sizes.split(',')]
        return []
    
    class Meta:
        ordering = ['-created_at']