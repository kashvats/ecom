from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .models import *
import random

from django.contrib import messages
import string
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm, authenticate
from django.contrib.auth import logout, login
from django.http import HttpResponse, HttpResponseRedirect, Http404


# Create your views here.
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def log_in(request):
    if request.method == 'POST':
        ak = AuthenticationForm(data=request.POST,request=request)
        if ak.is_valid():
            username = ak.cleaned_data.get('username')
            password = ak.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    else:
        ak = AuthenticationForm()
        return render(request, 'user/login.html', {'pl': ak})


def log_out(request):
    if request.user:
        logout(request)
        return redirect('product')
    else:
        return redirect('login')


def register(request):
    if request.method == 'POST':
        ak = regi(request.POST)
        if ak.is_valid():
            ak.save()
            messages.success(request,'user successfully created')
            return redirect('login')
        else:
            messages.error(request,'user not created due to values you gave or username already exist')
            return redirect('register')
    else:
        ak = regi()
        return render(request, 'user/register.html', {'pok': ak})


from random import shuffle

def homeview(request):
    categoy = category.objects.get(name='clothes')
    prod = item.objects.filter(cat_name=categoy)
    categ = category.objects.get(name='electronics')
    frod = item.objects.filter(cat_name=categ)
    return render(request, 'shop/product.html', {'prod': prod,'frod':frod})


def productview(request):
    prod = item.objects.all()
    return render(request, 'shop/product2.html', {'prod': prod})


def detailview(request, name):
    categ = category.objects.get(name='electronics')
    frod = item.objects.filter(cat_name=categ)
    prod = get_object_or_404(item,namee=name)
    return render(request, 'shop/detail.html', {'a': prod,'frod':frod})


def categoryview(request):
    cat = category.objects.all().order_by('name')
    return render(request, 'shop/cat_list.html', {'cat': cat})


def catprod(request,name):
    gro = category.objects.get(name=name)
    prod = item.objects.filter(cat_name=gro)
    return render(request, 'shop/cat_product.html', {'cat': prod})

@login_required(login_url='/login')
def cartsview(request):
    ca = cart.objects.filter(name=request.user)
    grand_total = 0
    print(ca)
    for a in ca:
        grand_total += a.price
    return render(request, 'shop/cart.html', {'cd': ca,'g':grand_total})

@login_required(login_url='/login')
def cartsedit(request, name):
    pro = item.objects.get(namee=name)
    ca = cart.objects.filter(item_name=pro)
    if ca:
        b = cart.objects.get(item_name=pro)
        if b.quantity > 1:
            b.quantity -= 1
            b.price = b.price - b.item_name.price
            b.save()
            messages.success(request,'product remove from cart')
            return HttpResponseRedirect('/cart')
        else:
            b.delete()
            messages.success(request,'product deleted from cart')
            return HttpResponseRedirect('/cart')


# product try view
@login_required(login_url='/login')
def producttryview(request, name):
    pro = item.objects.get(namee=name)
    if troy.objects.filter(item_name=pro).exists():
        messages.success(request, 'sorry sir this product is already on your try list')
        return redirect('try')
    elif troy.objects.create(user=request.user, item_name=pro):
        messages.success(request, 'product add to try list')
        return redirect('try')

@login_required(login_url='/login')
def triedview(request):
    tt = troy.objects.filter(user=request.user)
    return render(request, 'shop/try.html', {'tt': tt})

@login_required(login_url='/login')
def cartsdelete(request, name):
    pro = item.objects.get(namee=name)
    ca = cart.objects.filter(item_name=pro)
    if ca:
        b = cart.objects.get(item_name=pro)
        b.delete()
        messages.success(request, 'product deleted from cart')
        return HttpResponseRedirect('/cart')
    else:
        return HttpResponseRedirect('/product')


# add to cart
@login_required(login_url='/login')
def carts_item(request, name):
    pro = item.objects.get(namee=name)
    ca = cart.objects.filter(item_name=pro)
    if ca:
        b = cart.objects.get(item_name=pro)
        b.quantity += 1
        b.price += b.item_name.price
        b.save()
        messages.success(request, 'add to cart successfully')
        return HttpResponseRedirect('/cart')
    elif cart.objects.create(name=request.user, item_name=pro,price=pro.price):
        return HttpResponseRedirect('/cart')

@login_required(login_url='/login')
def checkoutview(request):
    try:
        loca = item.objects.all()
        ca = cart.objects.filter(name=request.user)
        if request.method == 'POST':
            ap = addresses(request.POST)
            if ap.is_valid():
                adress1 = ap.cleaned_data.get('address1')
                adress2 = ap.cleaned_data.get('address2')
                zip_code = ap.cleaned_data.get('zip_code')
                state = ap.cleaned_data.get('state')
                country = ap.cleaned_data.get('country')
                po = address(name=request.user, address1=adress1, address2=adress2, zip_code=zip_code, state=state,
                             country=country)

                po.save()
                pd = create_ref_code()
                for a in ca:
                    ak =a.item_name
                    pa = order.objects.create(itemss=ak,quantity=a.quantity,name=request.user, addressa=po, product_id=pd,ordered=True)
                    pa.save()
                ca.delete()
                return HttpResponseRedirect('/payment')
        else:
            ap = addresses()
            return render(request, 'shop/checkout.html', {'ap': ap})
    except ObjectDoesNotExist:
        return HttpResponse('object does not exist')

@login_required(login_url='/login')
def send_try(request, name):
    pro = item.objects.get(namee=name)
    ca = troy.objects.get(item_name=pro)
    if ca.tried_complete == True:
        messages.success(request, 'you already tried this product please choose another one')
        return HttpResponseRedirect('/try')
    elif ca:
        ca.tried_complete = True
        ca.save()
        messages.success(request, 'please give us reviews')
        return HttpResponseRedirect('/try')


    else:
        return HttpResponseRedirect('try')


def home(request):
    return render(request, 'shop/home.html')

# def curtaclan():
#     ak = len(cart.objects.filter(name=request.user))


def payme(request):
    ap = order.objects.filter(ordered=False)
    print(ap)
    return render(request, 'shop/payment.html')


def aboutus(request):
    return render(request, 'shop/payment.html')
def contact(request):
    return render(request, 'shop/payment.html')

def search(request):
    if request.method == 'GET':
        sear = request.GET['namee']
        ap = item.objects.filter(namee__startswith=sear)
        return render(request, 'shop/search.html',{'s':ap})
    else:
        return HttpResponse('thers noting here like that')
