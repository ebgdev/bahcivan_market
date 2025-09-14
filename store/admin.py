from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','created_date','is_avalible')
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','low_stock_threshold','stock_status','category','created_date','is_avalible')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]
    list_filter = ['category', 'is_avalible', 'created_date']
    search_fields = ['product_name', 'product_description']

    def stock_status(self, obj):
        if obj.is_out_of_stock():
            return "Out of Stock"
        elif obj.is_low_stock():
            return "Low Stock"
        else:
            return "In Stock"

    stock_status.short_description = 'Stock Status'

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'status', 'created_at']
    list_filter = ['rating', 'status', 'created_at']
    search_fields = ['product__product_name', 'user__username', 'subject']
    readonly_fields = ['ip']

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)

