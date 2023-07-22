from django.shortcuts import render,redirect,get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart,CartItem 
# from django.http import HttpResponse 

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
# to add product to cart one by one
def add_cart(request,product_id):
    #get the product
    product = Product.objects.get(id=product_id) 
    try:
        #get the cart using cart_id show up in the session
        cart = Cart.objects.get(cart_id = _cart_id(request)) 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request) 
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product ,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')


# to remove product added to cart one by one
def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# to remove whole product regardless of the amount
def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
        



def cart(request,total=0,quantity=0,cart_item=None):
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active= True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity+= cart_item.quantity
        
        #applying taxt 
        # tax = (18*total)/100
        # grand_total = total + tax        
    
    except ObjectNotExist:
        # just ignore
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        # 'tax' : tax ,
        # 'grand_total': grand_total,          
    }    

    return render(request,'store/cart.html/',context)