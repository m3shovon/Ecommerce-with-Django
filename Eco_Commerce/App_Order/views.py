from django.shortcuts import render, get_object_or_404, redirect
# messages
from django.contrib import messages
# Authentication
from django.contrib.auth.decorators import login_required
from App_Order.models import Cart, Order
from App_Shop.models import Product

# Create your views here.

@login_required 
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    # print("Item")
    # print(item)
    order_item = Cart.objects.get_or_create(user=request.user, item=item, purchased=False)
    # print("Order Item Object:")
    # print(order_item)
    # print(order_item[0])
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # print("Order Query Set")
    # print(order_qs)
    if order_qs.exists():
        order = order_qs[0] #converting order_qs to order
        # print("If Order exists")
        # print(order)
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This Item's Quantity is Updated")
            return redirect("App_Shop:home")
        else:
            order.order_items.add(order_item[0])
            messages.info(request, "This Item Was Added to your cart")
            return redirect("App_Shop:home")
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.info(request, "This Item was added to your cart")
        return redirect("App_Shop:home")




@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased= False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0] #convert from tuple to single item
        return render(request, 'App_Order/cart.html', context={'carts': carts , 'order': order})
    else:
        messages.warning(request, "You dont have any item in your cart")  
        return redirect('App_Shop:home')  

@login_required
def remove_from_cart(request,pk):
    item=get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item=order_item[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item is removed from your cart")
            return redirect("App_Order:cart")
        else:
            messages.info(request, "This item was not in your Cart")
            return redirect("App_Shop:home")           
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")

@login_required
def increase_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item=order_item[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.name} Quantity has been updated")
                return redirect("App_Order:cart")
        else:
            messages.info(request, f"{item.name} is not in your cart")        
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")


@login_required
def decreased_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs= Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order_item=order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.name} quantity has been updated") 
                return redirect("App_Order:cart")       
            else:
                order.order_items.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.name} has been removed from the cart")
                return redirect("App_Shop:home")
        else:
            messages.info(request, f"{item.name} is not in your cart")        
            return redirect("App_Shop:home")

    else:
        messages.info(request, "You don't have an active order")
        return redirect("App_Shop:home")



