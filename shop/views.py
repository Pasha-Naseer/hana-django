import random

from django.shortcuts import render, redirect
from .models import Collection, Product, Profile, Blog
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Used2B
# from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
# is
from .forms import ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
# from django.contrib.auth.models import User
from django.db.models import Q
from cart.cart import Cart
import json

# is
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserChangeForm, UserChangeFormUser
from utils import send_otp_code
from .models import OtpCode, User
from datetime import datetime, date, time, timedelta


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'اطلاعات کاربری آپدیت شد')
            return redirect("shop:shop_index")
        return render(request, 'shop/update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'برای دسترسی به این پیج باید وارد حساب شوید!')
        return redirect('shop:shop_index')


def blog(request):
    blog_list = Blog.objects.all()
    context = {"blog_list": blog_list}
    return render(request, 'shop/blog.html', context)


def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    context = {"blog": blog}
    return render(request, 'shop/blog_detail.html', context)


def shop_index(request):
    latest_collection_list = Collection.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    famous_product_list = Product.objects.filter(Q(name__icontains='Simple') | Q(name__icontains='Nivea') |
                                                 Q(name__icontains='Loreal') | Q(name__icontains='Euphoria'))[:4]
    blog_list = Blog.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:3]
    context = {"latest_collection_list": latest_collection_list,
               'famous_product_list': famous_product_list,
               'blog_list': blog_list}
    return render(request, "shop/shop_index.html", context)


def products_index(request, collection_id):
    products_list = Product.objects.filter(pub_date__lte=timezone.now(), collection=collection_id).order_by("-pub_date")
    collection = Collection.objects.get(pk=collection_id)
    context = {"products_list": products_list,
               "collection": collection,}
    return render(request, "shop/products.html", context)


def products_detail(request, collection_id, product_id):
    product = Product.objects.get(pk=product_id)
    context = {"product": product}
    return render(request, "shop/products_detail.html", context)


def about(request):
    return render(request, 'shop/about.html', {})


def user_login(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from the database
            saved_cart = current_user.old_cart
            if saved_cart:
                # convert to dict using json
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                # loop through the cart and add items from the database
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, "شما با موفقیت به حساب وارد شدید")
            return redirect("shop:shop_index")
        else:
            messages.error(request, "خطایی در حین ورود به حساب رخ داد")
            return redirect('shop:login')
    else:
        return render(request, 'shop/login.html', {})


def user_logout(request):
    logout(request)
    messages.success(request, "شما با موفقیت از حساب خارج شدید")
    return redirect("shop:login")

# Used2B
# def user_register(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, 'User Created - Please fill out your user info below')
#             return redirect('shop:update_info')
#         else:
#             messages.error(request, 'There was an error during the registration process')
#             return redirect('shop:register')
#     else:
#         return render(request, 'shop/register.html', {'form': form})


# is
class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request,'shop/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            while OtpCode.objects.filter(phone_number=form.cleaned_data['phone_number']).exists():
                OtpCode.objects.get(phone_number=form.cleaned_data['phone_number']).delete()
            random_code = random.randint(1000, 9999)

            send_otp_code(form.cleaned_data['phone_number'], random_code)

            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'username': form.cleaned_data['my_username'],
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['my_email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'کدی برای شما ارسال شد', 'success')
            return redirect('shop:verify_code')
        return redirect('shop:shop_index')


# is
class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'shop/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            if not code_instance.calculate_date() == datetime.now().date():
                messages.error(request, 'کد منقضی شد!', 'danger')
                return redirect('shop:register')
            substraction = datetime.combine(date.today(), datetime.now().time()) - datetime.combine(date.today(), code_instance.calculate_time())
            scale = time(0, 3, 0, 0)
            duration = timedelta(hours=scale.hour, minutes=scale.minute, seconds=scale.second,
                          microseconds=scale.microsecond)
            #print(datetime.now().time())
            #print(code_instance.calculate_time())
            #print(substraction)
            #print(duration)
            if substraction > duration:
                messages.error(request, 'کد منقضی شد!', 'danger')
                return redirect('shop:register')
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['username'], user_session['phone_number'],
                                         user_session['email'], user_session['first_name'], user_session['last_name'],
                                         user_session['password'],)
                code_instance.delete()
                messages.success(request, 'کاربر با موفقیت ثبت شد', 'success')
                username = user_session['username']
                password = user_session['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('shop:shop_index')
            else:
                messages.error(request, "کد اشتباه!", 'danger')
                return redirect('shop:verify_code')
        return render(request, 'shop/register.html', {'form': form})


def user_update(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserChangeFormUser(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'کاربر آپدیت شد')
            return redirect("shop:shop_index")
        return render(request, 'shop/update_user.html', {'user_form': user_form})
    else:
        messages.error(request, 'برای ورود به پیج باید وارد حساب شوید!')
        return redirect('shop:shop_index')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill the form?
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز شما آپدیت شد!')
                return redirect('shop:login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('shop:update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'shop/update_password.html', {'form': form})
    else:
        messages.error(request, 'برای ورود به پیج باید وارد حساب شوید!')
        return redirect('shop:shop_index')


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(collection__name__icontains=searched) | Q(collection__description__icontains=searched))
        if not searched:
            messages.success(request, "Product does not exist")
            return render(request, 'shop/search.html', )
        else:
            return render(request, 'shop/search.html', {'searched': searched})
    else:
        return render(request, 'shop/search.html', {})
