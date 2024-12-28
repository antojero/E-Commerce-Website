from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
import json
# Create your views here.

def display(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})

def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = CustomUserCreationForm()
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registration Successful Now login")
                return redirect("/login")
            else:
                messages.error(request, "Registration Failed")
        return render(request, "shop/register.html", {"form": form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request,username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect("/")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("/login")
        return render(request, "shop/login.html")
   

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successful")
        return redirect("/")
    else:
        messages.error(request, "You are not logged in")
        return redirect("/login")
def collections(request):
    category = Catagory.objects.all()
    return render(request, "shop/collections.html", {'category': category})

def collectionsview(request, name):
    if (Catagory.objects.filter(name=name,status=0)):
        product = Product.objects.filter(category__name=name)
        return render(request, "shop/products/collectionsview.html", {'product': product,"category_name":name})
    else:
        messages.warning(request, "No category found")
        return redirect("collection")
    
def productview(request, cname, pname):
    if (Catagory.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            product = Product.objects.get(name=pname,status=0)
            return render(request, "shop/products/productview.html", {'products': product})
        else:
            messages.warning(request, "No product found")
            return redirect("collectionsview")
    else:
        messages.warning(request, "No category found")
        return redirect("collectionview")
    
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user)
        return render(request, "shop/cart.html", {'cart': cart})
    else:
        return redirect("/")
    
def remove_from_cart(request,id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(id=id)
        cart.delete()
        return redirect("/cart_page")
    else:
        return redirect("/")

    
def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data.get('product_qty')
            print(product_qty)
            product_id = data.get("pid")
            #print(request.user.id)
            product_status = Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(product_id=product_id,user=request.user):
                    return JsonResponse({"status":"Product already in cart"},status = 200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user, product_id = product_id, product_qty = product_qty)
                        return JsonResponse({'status':'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Stack Not available'}, status=200)
            return JsonResponse({'status':'Succes'}, status=200)
        else:
            return JsonResponse({'status':'Login to add cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
 
