from django.shortcuts import render
from store.models import Product, Banner



def home(request):
    products = Product.objects.all().filter(is_avalible = True)
    banners = Banner.objects.filter(is_active=True).order_by('order', '-created_at')

    context = {
        'products' : products,
        'banners': banners,
    }


    return render(request,'home.html',context)