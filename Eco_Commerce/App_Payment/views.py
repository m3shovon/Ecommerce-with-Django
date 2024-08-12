from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from App_Order.models import Order, Cart
from App_Payment.forms import BillingAddress
from App_Payment.forms import BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# for sslcommerz payment
# import requests
# from sslcommerz_lib import SSLCOMMERZ
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address) #form generate from Saved Address
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved")
    order_qs = Order.objects.filter(user=request.user, ordered = False)     
    orderItems = order_qs[0].order_items.all()
    order_total = order_qs[0].get_totals() #Order>model>get_totals
    return render(request, 'App_Payment/checkout.html', context={'form':form, "order_items": orderItems, "order_total": order_total, "saved_address": saved_address})



@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    if not saved_address[0].is_fully_filled():
        messages.info(request, f"Please complete shipping address!")
        return redirect("App_Payment:checkout")

    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Complete Profile Details")
        return redirect("App_Login:profile")


        # sslcz = SSLCOMMERZ({ 'store_id': 'ecoco63c3c9f981ff6', 'store_pass': 'ecoco63c3c9f981ff6@ssl', 'issandbox': True })

    ### SSLCOMMERZ GETWAY ###   
    # store_id = "ecoco63c3c9f981ff6"
    # store_pass = "ecoco63c3c9f981ff6@ssl"
    # mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

    # status_url = request.build_absolute_url(reverse("App_Payment:complete"))

    # mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    # mypayment.set_product_integration(total_amount=Decimal('20.20'), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=2, shipping_method='YES', product_profile='None')

    # mypayment.set_customer_info(name='John Doe', email='johndoe@email.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01711111111')

    # mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')

    # response_data = mypayment.init_payment()

    return render(request, "App_Payment/payment.html", context={})




@csrf_exempt
def complete(request):
    if request.method == "POST" or request.method == "post":
        payment_data = request.POST
        status = payment_data['status']     
             
        # bank_tran_id = payment_data['bank_tran_id']     

        if status == 'VALID':
            val_id = payment_data['val_id']     
            tran_id = payment_data['tran_id']
            messages.success(request, f"Your Payment is completed")
            return HttpResponseRedirect(reverse("App_Payment:purchase", kwargs={"val_id":val_id,'tran_id':tran_id }))
        elif status == 'FAILED':
            messages.danger(request, f"Your Payment is failed. Please, Try Again!")    
    return render(request, "App_Payment/complete.html", context={})


# After Purchase order completion
@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orederId = orderId
    order.paymentId = val_id 
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased = False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("App_Shop:home"))


@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered = True)
        context = {"orders": orders}

    except:
        messages.warning(request, f"You don't have any active order!")
        return redirect("App_Shop:home") 
    return render(request, "App_Payment/order.html", context={})







