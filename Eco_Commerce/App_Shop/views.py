from django.shortcuts import render
# Create your views here.
from App_Shop.models import Product 
# Import Views
from django.views.generic import ListView, DetailView
#mixin
from django.contrib.auth.mixins import LoginRequiredMixin
# user log
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from App_Shop.models import Product
# from App_UserLog.models import UserLog

class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'
    # by default context value is : object_list


class ProductDetail(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'App_Shop/product_details.html'  
        # by default context value is : object

# @login_required
# def cart_add(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     # add the product to the user's cart here
    
#     # log the user's action
#     UserLog.objects.create(user=request.user, action='added to cart', product=product)
    
#     return redirect('cart_detail')