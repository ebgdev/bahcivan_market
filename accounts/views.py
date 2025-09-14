from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account
# verificaion email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = "Lütfen hesabınızı aktifleştiriniz"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user) ,
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # messages.success(request,'Lütfen hesabınızı etkinleştirmek için size gönderilen e-postayı onaylayınız')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # Getting the product variations by cart id 
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation)) #by default it's queryset so we make it list


                    #Get the cart items from the user to access user product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request,user)
            messages.success(request,'Giriş Yapıldı')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'Geçersiz giriş')
            return redirect('login')
    
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Çıkış yapıldı')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Tebrikler! kaydınız başarıyla tamamlandı.')
        return redirect('login')
    else:
        messages.error(request,'Geçersiz aktivasyon bağlantısı')
        return redirect('register')
    

@login_required(login_url = 'login')
def dashboard(request):
    from orders.models import Order, OrderProduct

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()

    context = {
        'orders_count': orders_count,
        'user': request.user,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url = 'login')
def my_orders(request):
    from orders.models import Order

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url = 'login')
def order_detail(request, order_id):
    from orders.models import Order, OrderProduct

    order_detail = Order.objects.get(user=request.user, is_ordered=True, order_number=order_id)
    order_product = OrderProduct.objects.filter(order=order_detail)

    context = {
        'order_detail': order_detail,
        'order_product': order_product,
        'subtotal': (order_detail.order_total + order_detail.tax),
    }
    return render(request, 'accounts/order_detail.html', context)

@login_required(login_url = 'login')
def edit_profile(request):
    from .models import UserProfile
    from .forms import UserForm, UserProfileForm

    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url = 'login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Şifreniz başarıyla güncellendi.')
                return redirect('change_password')
            else:
                messages.error(request, 'Mevcut şifrenizi yanlış girdiniz.')
                return redirect('change_password')
        else:
            messages.error(request, 'Şifreler eşleşmiyor.')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact = email)

            # reset password email
            current_site = get_current_site(request)
            mail_subject = "Lütfen şifrenizi yenileyiniz"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user) ,
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Şifre sıfırlama bağlantısı e-posta adresinize gönderildi')
            return redirect('login')
        else:
            messages.error(request,'Hesap bulunmamaktadır')
            return redirect('forgetPassword')

    return render(request,'accounts/forgetPassword.html')



def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Lütfen şifrenizi yenileyiniz')
        return redirect('resetPassword')
    else:
        messages.error(request,'Bu bağlantı süresi doldu!')
        return redirect('login')



def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_passowrd = request.POST['confirm_password']

        if password == confirm_passowrd:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Şifre başarılı bir şekilde yenilendi')
            return redirect('login')

        else:
            messages.error(request,'Şifre eşleşmedi')
            return redirect('resetPassword')

    return render(request,'accounts/resetPassword.html')