from django.contrib import admin
from .models import WishList

@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__product_name']
    readonly_fields = ['created_at']
