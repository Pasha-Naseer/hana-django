from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from shop.models import Profile
from django.contrib import messages
from django.views import View
from django.conf import settings
import requests
import json
import time
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
# used2B

# from django.contrib.auth.models import User
from shop.models import Product
import datetime

# is
# ZARINPAL

from shop.models import User


# was is_superuser
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_admin:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the OrderItems
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == "true":
                order = Order.objects.filter(id=pk)
                # update status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)

                messages.success(request, "اطلاعات ارسال آپدیت شد")
                return redirect('payment:not_shipped_dash')
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
                messages.success(request, "اطلاعات ارسال آپدیت شد")
                return redirect('payment:shipped_dash')

        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.error(request, 'Access Denied')
        return redirect('shop:shop_index')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_admin:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # update status
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)

            messages.success(request, "اطلاعات ارسال آپدیت شد")
            return redirect('payment:not_shipped_dash')

        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, "خطای دسترسی!")
        return redirect('shop:shop_index')


# was request.user.is_superuser
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_admin:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # update status
            now = datetime.datetime.now()
            order.update(shipped=False)

            messages.success(request, "اطلاعات ارسال آپدیت شد")
            return redirect('payment:shipped_dash')
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, "خطای دسترسی!")
        return redirect('shop:shop_index')


# def process_order(request):
#     if request.POST:
#         # Get Card
#         cart = Cart(request)
#         cart_products = cart.get_prods
#         quantities = cart.get_quants
#         totals = cart.cart_total()
#
#         payment_form = PaymentForm(request.POST or None)
#         # Get shipping session data
#         my_shipping = request.session.get('my_shipping')
#         # gather order info
#
#         # create shipping address from session info
#         full_name = my_shipping['shipping_full_name']
#         email = my_shipping['shipping_email']
#         shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}\n"
#         amount_paid = totals
#         # create order
#         if request.user.is_authenticated:
#             user = request.user
#             # create order
#             create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
#                                  amount_paid=amount_paid)
#             create_order.save()
#
#             # Get product info
#             order_id = create_order.pk
#             for product in cart_products():
#                 product_id = product.id
#                 # get product price
#                 if product.is_available:
#                     if product.has_discount:
#                         price = product.price_with_discount()
#                     else:
#                         price = product.price
#                 else:
#                     # ???????????????
#                     price = product.price
#
#                 # get quantity
#                 for key, value in quantities().items():
#                     if int(key) == product.id:
#                         # create OrderItem
#                         create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
#                                                       quantity=value, price=price)
#                         create_order_item.save()
#
#             # clear cart
#             for key in list(request.session.keys()):
#                 if key == 'session_key':
#                     # delete key
#                     del request.session[key]
#             # Delete cart from database (old cart field)
#             current_user = Profile.objects.filter(user__id=request.user.id)
#             # Delete shopping un database (old_cart fields)
#             current_user.update(old_cart="")
#
#             messages.success(request, "سفارش به ثبت رسید")
#             return redirect('shop:shop_index')
#         else:
#             # not logged in
#             create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
#                                  amount_paid=amount_paid)
#             create_order.save()
#             # Get product info
#             order_id = create_order.pk
#             for product in cart_products():
#                 product_id = product.id
#                 # get product price
#                 if product.is_available:
#                     if product.has_discount:
#                         price = product.price_with_discount()
#                     else:
#                         price = product.price
#                 else:
#                     # ???????????????
#                     price = product.price
#
#                 # get quantity
#                 for key, value in quantities().items():
#                     if int(key) == product.id:
#                         # create OrderItem
#                         create_order_item = OrderItem(order_id=order_id, product_id=product_id,
#                                                       quantity=value, price=price)
#                         create_order_item.save()
#
#             for key in list(request.session.keys()):
#                 if key == 'session_key':
#                     # delete key
#                     del request.session[key]
#
#             messages.success(request, "سفارش به ثبت رسید")
#             return redirect('shop:shop_index')
#
#
#     else:
#         messages.error(request, "خطای دسترسی!")
#         return redirect('shop:shop_index')
#

#
# def billing_info(request):
#     if request.POST:
#         cart = Cart(request)
#         cart_products = cart.get_prods
#         quantities = cart.get_quants
#         totals = cart.cart_total()
#
#         # create a session with shipping info
#         my_shipping = request.POST
#         request.session['my_shipping'] = my_shipping
#
#         # check to see if the user is logged in
#         if request.user.is_authenticated:
#             # get the billing form
#             billing_form = PaymentForm()
#             return render(request, 'payment/billing_info.html', {'cart_products': cart_products,
#                                                                  'quantities': quantities,
#                                                                  'totals': totals,
#                                                                  'shipping_info': request.POST,
#                                                                  "billing_form": billing_form})
#         # not logged in
#         else:
#             billing_form = PaymentForm()
#             return render(request, 'payment/billing_info.html', {'cart_products': cart_products,
#                                                                  'quantities': quantities,
#                                                                  'totals': totals,
#                                                                  'shipping_info': request.POST,
#                                                                  "billing_form": billing_form})
#
#         # shipping_form = request.POST
#         #return render(request, 'payment/billing_info.html', {'cart_products': cart_products,
#                                                              #'quantities': quantities,
#                                                              #'totals': totals,
#                                                              #'shipping_form': shipping_form})
#     else:
#         messages.error(request, "خطای دسترسی!")
#         return redirect("shop:shop_index")

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/payment/payment_verify/'
phone = 'YOUR_PHONE_NUMBER'
class OrderPayView(View):
    def get(self, request):
        return redirect('payment:checkout')
    def post(self, request):

        cart = Cart(request)
        totals = cart.cart_total()

        data = {
            'MerchantID': settings.MERCHANT,
            'Amount': int(totals),
            'Description': description,
            #"Phone": phone,
            'CallbackURL': CallbackURL,

        }
        data = json.dumps(data)

        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)


            if response.status_code == 200:
                response = response.json()

                if response['Status'] == 100:
                    my_shipping = request.POST
                    request.session['my_shipping'] = my_shipping
                    # return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response['data']['authority']), 'authority': response['data']['authority']})
                    return HttpResponseRedirect(ZP_API_STARTPAY + str(response['Authority']))
                else:
                    return JsonResponse({'status': False, 'code': str(response['Authority'])})

            return HttpResponse(response)

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})




# def payment_verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": '',
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return JsonResponse({'status': True, 'RefID': response['RefID']})
#         else:
#             return JsonResponse({'status': False, 'code': str(response['Status'])})
#     return HttpResponse(response)
class OrderVerifyView(View):
    def get(self, request):
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        print(request.GET)
        t_status = request.GET['Status']
        t_authority = request.GET['Authority']
        if request.GET['Status'] == 'OK':
            data = {
                    "MerchantID": settings.MERCHANT,
                    "Amount": int(totals),
                    "Authority": t_authority,
                }
            data = json.dumps(data)
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}
            response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

            my_shipping = request.session.get('my_shipping')
            print(request.session.get('my_shipping'))
            # gather order info

            # create shipping address from session info
            full_name = my_shipping['shipping_full_name']
            email = my_shipping['shipping_phone']
            shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n"
            amount_paid = totals
            # create order
            if request.user.is_authenticated:
                user = request.user
                # create order
                create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address,
                                     amount_paid=amount_paid)
                create_order.save()

                # Get product info
                order_id = create_order.pk
                for product in cart_products():
                    product_id = product.id
                    # get product price
                    if product.is_available:
                        if product.has_discount:
                            price = product.price_with_discount()
                        else:
                            price = product.price
                    else:
                        # ???????????????
                        price = product.price

                    # get quantity
                    for key, value in quantities().items():
                        if int(key) == product.id:
                            # create OrderItem
                            create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,
                                                          quantity=value, price=price)
                            create_order_item.save()

                # clear cart
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        # delete key
                        del request.session[key]
                # Delete cart from database (old cart field)
                current_user = Profile.objects.filter(user__id=request.user.id)
                # Delete shopping un database (old_cart fields)
                current_user.update(old_cart="")

                messages.success(request, "سفارش به ثبت رسید")

                return redirect('shop:shop_index')
            else:
                # not logged in
                create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                     amount_paid=amount_paid)
                create_order.save()
                # Get product info
                order_id = create_order.pk
                for product in cart_products():
                    product_id = product.id
                    # get product price
                    if product.is_available:
                        if product.has_discount:
                            price = product.price_with_discount()
                        else:
                            price = product.price
                    else:
                        # ???????????????
                        price = product.price

                    # get quantity
                    for key, value in quantities().items():
                        if int(key) == product.id:
                            # create OrderItem
                            create_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                          quantity=value, price=price)
                            create_order_item.save()

                for key in list(request.session.keys()):
                    if key == 'session_key':
                        # delete key
                        del request.session[key]

                messages.success(request, "سفارش به ثبت رسید")

                return redirect('shop:shop_index')
            return HttpResponse("خطای پرداخت!")


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products,
                                                         'quantities': quantities,
                                                         'totals': totals,
                                                         'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products,
                                                         'quantities': quantities,
                                                         'totals': totals,
                                                         'shipping_form': shipping_form})
