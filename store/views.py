from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db.models import Q
from .models import Product
from category.models import Category
from carts.views import _cart_id ,CartItem
# from carts.models import CartItem

def store(request,category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug =category_slug)
        products = Product.objects.filter(category = categories, is_avalible = True)
        paginator = Paginator(products,9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_avalible = True).order_by('id')
        paginator = Paginator(products,9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request,'store/store.html/',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug= category_slug,slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
    }
    return render(request,'store/product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Use Q objects to perform an OR query on multiple fields
            products = Product.objects.filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)
            ).order_by('-created_date')
            product_count = products.count()
    # else:
    #     products = []  # Initialize an empty list if no keyword is provided

    context = {
        'products': products,
        'product_count': product_count ,
    }
    return render(request, 'store/store.html', context)