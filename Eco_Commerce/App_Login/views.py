from django.shortcuts import render,HttpResponseRedirect
# Create your views here.
from django.urls import reverse 
from django.http import HttpResponse
# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# form and model
from App_Login.models import Profile
from App_Login.forms import ProfileForm, SignUpForm
# Message
from django.contrib import messages #error, success, info, warning

# SIGN UP
def sign_up(request):
    form = SignUpForm()
    if request.method == "POST":
        form =  SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/signup.html', context={'form':form})        

# SIGN IN
def login_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') #email is treated as username in model.py
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) 
                return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request, 'App_Login/login.html', context={'form': form})

# SIGNOUT
@login_required
def logout_user(request):
     logout(request)
     messages.warning(request, "You are Logged Out")
     return HttpResponseRedirect(reverse('App_Shop:home'))

# Profile 
@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form=ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Change Saved!")

            form=ProfileForm(instance=profile)
    return render(request, 'App_Login/change_profile.html', context={'form': form})        




