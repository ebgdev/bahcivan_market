from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery, Banner
from django.utils.html import format_html
import os

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

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'link_type', 'get_link_target', 'is_active', 'order', 'created_at', 'load_to_banner_button')
    list_filter = ('link_type', 'is_active', 'created_at')
    search_fields = ('title',)
    list_editable = ('is_active', 'order')
    ordering = ('order', '-created_at')

    fieldsets = (
        ('Banner Information', {
            'fields': ('title', 'image', 'is_active', 'order')
        }),
        ('Link Configuration', {
            'fields': ('link_type', 'category', 'product', 'custom_url'),
            'description': 'Choose link type and configure the corresponding field'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return 'No Image'
    image_preview.short_description = 'Preview'

    def get_link_target(self, obj):
        if obj.link_type == 'category' and obj.category:
            return f"Category: {obj.category.category_name}"
        elif obj.link_type == 'product' and obj.product:
            return f"Product: {obj.product.product_name}"
        elif obj.link_type == 'url' and obj.custom_url:
            return f"URL: {obj.custom_url}"
        return 'No Link'
    get_link_target.short_description = 'Link Target'

    def load_to_banner_button(self, obj):
        return format_html(
            '<button type="button" onclick="loadToBanner({})" class="button">Load to Banner</button>',
            obj.id
        )
    load_to_banner_button.short_description = 'Actions'

    class Media:
        js = ('admin/js/banner_admin.js',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Add JavaScript for dynamic field display
        form.base_fields['link_type'].widget.attrs.update({
            'onchange': 'toggleLinkFields(this.value)'
        })

        return form

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Banner, BannerAdmin)

