# from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Cart, CartItem, Coupon

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_items_count', 'get_total', 'updated_at']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items'
    
    def get_total(self, obj):
        return f"${obj.get_total()}"
    get_total.short_description = 'Total'

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percentage', 'active', 'valid_from', 'valid_to']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']