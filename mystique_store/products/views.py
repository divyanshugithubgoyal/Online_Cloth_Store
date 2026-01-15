from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, Category

def product_list_view(request):
    """Display all products with category filtering and search"""
    products = Product.objects.all()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')
    
    # Filter by category
    if category_filter and category_filter != 'ALL':
        products = products.filter(category__name=category_filter)
    
    # Search functionality
    if search_query:
        products = products.filter(
            name__icontains=search_query
        ) | products.filter(
            description__icontains=search_query
        ) | products.filter(
            category__name__icontains=search_query
        )
    
    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail_view(request, slug):
    """Display single product detail"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def category_products_view(request, slug):
    """Display products by category"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
    }
    return render(request, 'products/category_products.html', context)

def search_api_view(request):
    """API endpoint for live search"""
    query = request.GET.get('q', '')
    
    if len(query) < 3:
        return JsonResponse({'products': []})
    
    products = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        description__icontains=query
    )
    
    products = products[:5]  # Limit to 5 results
    
    products_data = [{
        'name': p.name,
        'slug': p.slug,
        'price': str(p.price),
        'image': p.image.url if p.image else '',
    } for p in products]
    
    return JsonResponse({'products': products_data})