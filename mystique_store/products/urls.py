from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('search-api/', views.search_api_view, name='search_api'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('<slug:slug>/', views.product_detail_view, name='product_detail'),
]