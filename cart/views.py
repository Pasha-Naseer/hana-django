from django.shortcuts import render, get_object_or_404, redirect, reverse
from .cart import Cart
from shop.models import Product, ProductCode
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_dict = cart.get_quants()  # {'3': 1, '3-12': 2}

    cart_items = []

    for key, qty in cart_dict.items():
        if '-' in key:
            product_id, code_id = key.split('-')
            product = Product.objects.get(id=product_id)
            code = ProductCode.objects.get(id=code_id)
        else:
            product = Product.objects.get(id=key)
            code = None

        cart_items.append({
            'key': key,
            'product': product,
            'code': code,
            'quantity': qty,
        })

    totals = cart.cart_total()
    print(cart_items)
    return render(request, 'cart/cart_summary.html', {
        'cart_items': cart_items,
        'totals': totals
    })



def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        code_id = request.POST.get('product_code_id')  # matches your template
        # print("id", product_id)
        # print("qty", product_qty)
        # print("code", code_id)
        p = get_object_or_404(Product, pk=product_id)
        if p.quantity - product_qty < 0:
            messages.error(request, "تعداد مورد نظر شما موجود نمی باشد، لطفا تعداد درخواستی را تغییر دهید و دوباره امتحان کنید")
            return HttpResponseRedirect(reverse("shop:products_detail", (p.collection.id, p.id, )))
        # Pass code_id directly to Cart.add
        cart.add(key=product_id, quantity=product_qty, code_id=code_id)
        return JsonResponse({'qty': len(cart)})


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        cart_key = request.POST.get('product_id')  # could be "3" or "3-12"

        # pass as positional argument
        cart.delete(cart_key)

        return JsonResponse({'product': cart_key})




def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        cart_key = request.POST.get('product_id')  # string key like "3" or "3-12"
        product_qty = int(request.POST.get('product_qty'))

        # pass as positional arguments
        cart.update(cart_key, product_qty)

        return JsonResponse({'qty': product_qty})
