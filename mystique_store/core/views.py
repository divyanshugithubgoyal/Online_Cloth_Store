# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from products.models import Product, Category

def home_view(request):
    """Homepage with featured products and categories"""
    featured_products = Product.objects.filter(featured=True)[:8]
    categories = Category.objects.all()
    
    # Get products by category for featured section
    kids_female = Product.objects.filter(category__name='KIDS_FEMALE')[:4]
    kids_male = Product.objects.filter(category__name='KIDS_MALE')[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'kids_female': kids_female,
        'kids_male': kids_male,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    """About page"""
    return render(request, 'core/about.html')

def contact_view(request):
    """Contact page"""
    return render(request, 'core/contact.html')