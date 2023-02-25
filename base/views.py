from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required

from .models import Restaurant, Item, Order, OrderItem, RestaurantLocation, UserAdress
from .models import TYPES_OF_RESTAURANTS,VALUES

import googlemaps
import json
from datetime import datetime

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    #login management
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found!')

        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
            messages.info(request,f'Hello {username}')
        else:
            messages.error(request,'Wrong username or password!')
    return render(request,'base/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    entry_type = request.GET.get('t','')
    entry_value = request.GET.get('v','')
    types_of_restaurants = TYPES_OF_RESTAURANTS
    restaurant_values = VALUES
    
    if entry_value:
        restaurant_list = Restaurant.objects.filter(value=entry_value)
    elif entry_type:
        restaurant_list = Restaurant.objects.filter(type=entry_type)
    else:  
        restaurant_list = Restaurant.objects.all()

    context = {
        'restaurants':restaurant_list,
        'types_of_restaurants': types_of_restaurants,
        'restaurant_values': restaurant_values,
    }
    
    return render(request,'base/home.html',context)

@login_required(login_url="login") 
def restaurant(request,pk):
    #filtering items for specific restaurant id
    item_list = Item.objects.filter(place__id=pk)
    order = Order.objects.filter(user__username=request.user,completed=False)[0]
    print(order)
    #adding and removing in order with buttons
    if request.method == "POST":
        data = request.POST
        if 'add-to-order' in request.POST:
            data = data['add-to-order']
            item = OrderItem.objects.filter(items__id=data)[0]
            #adding items
            print(data)
            if order.items and item:
                if len(order.items.all()) > 0:
                    if order.items.all()[0].items.place == item.items.place:
                        order.items.add(item)
                        item.quanity_for_order += 1
                        item.save()
                    else:
                        messages.info(request, 'item is from diffrent restaurant than your order!')
                        
                else:
                    order.items.add(item)
                    item.quanity_for_order += 1
                    item.save()
                    
        
        elif "remove-from-order" in data:
            data = data["remove-from-order"]
            item = OrderItem.objects.filter(id=data)[0]
            if item and order and item.quanity_for_order > 0:
                item.quanity_for_order -= 1
                if item.quanity_for_order == 0:
                    order.items.remove(item)
                item.save()
                
    context = {'items': item_list,
               'order_items':order.items.all(),
               'order':order
               }  
    
    return render(request,'base/restaurant.html',context)

@login_required(login_url="login") 
def orders(request):
    return render(request,'base/orders.html')

@login_required(login_url="login") 
def account(request):
    return render(request,'base/account.html')

@login_required(login_url="login") 
def checkout(request):
    #distance
    gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
    order = Order.objects.filter(pk=1)[0]
    user_address = UserAdress.objects.filter(pk=1)[0]
    order_items = order.items.all()
    restaurant = None
    result_restaurant = None
    result_user = None
    result_city = None
    calculate_distance = 0.0
    calculate_duration = 0.0
    if order.items.all():
        #check in which restaurant is item
        restaurant = order.items.all()[0].items.place

        result_city = json.dumps(gmaps.geocode(str(f' {restaurant.location.city}')))
        result_city = json.loads(result_city)[0]['geometry']['location']
        
        result_restaurant = json.dumps(gmaps.geocode(str(f'{restaurant.location.street}, {restaurant.location.postcode} {restaurant.location.country} {restaurant.location.city}')))
        result_restaurant = json.loads(result_restaurant)[0]['geometry']['location']
        
        result_user = json.dumps(gmaps.geocode(str(f'{user_address.street}, {user_address.postcode} {user_address.country} {user_address.city}')))
        result_user = json.loads(result_user)[0]['geometry']['location']

        now = datetime.now()
        calculate = json.dumps(gmaps.distance_matrix(result_city,
                            result_restaurant,
                            mode="driving",
                            departure_time=now))
        calculate_duration = json.loads(calculate)['rows'][0]['elements'][0]['duration']['text'][0:2]
        calculate_distance = json.loads(calculate)['rows'][0]['elements'][0]['distance']['text'][0:3]
        calculate_duration = int(calculate_duration)+15
        print(calculate_distance)
        
        
    #remove item from order
    if request.method == "POST":
        data = request.POST
        data = data["remove-from-order"]
        item = OrderItem.objects.filter(id=data)[0]
        order = Order.objects.filter(pk=1)[0]
        if item and order and item.quanity_for_order > 0:
            item.quanity_for_order -= 1
            if item.quanity_for_order == 0:
                order.items.remove(item)
            item.save()

    #calculation delivery price 2 zl per km
    order.delivery_price = round(2*float(calculate_distance),2)
    order.save()

    #calculating copmbined price
    price = 0
    for item in order_items:
        if item:
            price += item.quanity_for_order * item.items.price
    order.combined_price = float(price) + order.delivery_price
    order.save()

    context = {
        'order_items':order_items,
        'order':order,'restaurant':restaurant,
        'restaurant_location':result_restaurant,
        'city_location':result_city,
        'user_location':result_user,
        'calculate_distance':calculate_distance,
        'calculate_duration':calculate_duration
        }
    return render(request,'base/checkout.html',context)

