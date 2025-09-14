from django.contrib import admin
from .models import Account, UserProfile, Address
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'country']
    search_fields = ['user__username', 'city', 'state', 'country']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'first_name', 'last_name', 'city', 'state', 'is_default']
    list_filter = ['address_type', 'is_default', 'country']
    search_fields = ['user__username', 'first_name', 'last_name', 'city']

admin.site.register(Account,AccountAdmin)