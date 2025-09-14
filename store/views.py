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
    products = Product.objects.filter(is_avalible=True)
    product_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = products.filter(
                Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)
            )

    # Price filtering
    if 'min_price' in request.GET and request.GET['min_price']:
        min_price = request.GET['min_price']
        products = products.filter(price__gte=min_price)

    if 'max_price' in request.GET and request.GET['max_price']:
        max_price = request.GET['max_price']
        products = products.filter(price__lte=max_price)

    # Category filtering
    if 'category' in request.GET and request.GET['category']:
        category_id = request.GET['category']
        products = products.filter(category__id=category_id)

    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_date')
    elif sort_by == 'rating':
        # Order by average rating (requires aggregation)
        from django.db.models import Avg
        products = products.annotate(avg_rating=Avg('reviewrating__rating')).order_by('-avg_rating')
    else:
        products = products.order_by('product_name')

    product_count = products.count()

    # Pagination
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': product_count,
        'keyword': request.GET.get('keyword', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'selected_category': request.GET.get('category', ''),
        'sort_by': sort_by,
    }
    return render(request, 'store/store.html', context)