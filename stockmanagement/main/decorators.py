from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect


def authentcateduser(func_view):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            messages.error(request,f"You are already logged in")
            return redirect('home')
        else:
            return func_view(request,*args,**kwargs)
    return wrapper_func


def shop_acounts(func_view):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_superuser == False:
            messages.error(request,f"You are not allowed to view this page")
            return redirect('shop_home')
        else:
            return func_view(request,*args,**kwargs)
    return wrapper_func

