from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required

from .forms import AddressForm
from .models import Restaurant, Item, Order, OrderItem, RestaurantLocation, UserAdress
from .models import TYPES_OF_RESTAURANTS,VALUES

import googlemaps
import json
from datetime import datetime

#login view
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

#logout view
def logoutUser(request):
    logout(request)
    return redirect('home')

#home view
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

#restaurant view
@login_required(login_url="login") 
def restaurant(request,pk):
    #filtering items for specific restaurant id
    item_list = Item.objects.filter(place__id=pk)
    order, created = Order.objects.get_or_create(user=request.user,completed=False)
    #adding and removing in order with buttons
    if request.method == "POST":
        data = request.POST
        if 'add-to-order' in request.POST:
            data = data['add-to-order']
            item = Item.objects.filter(id=data).first()    
            #try to get first object if exists
            try: 
                order_item = OrderItem.objects.filter(items__id=item.id,order__id=order.id).first()    
                quanity = order_item.quanity+1
        
            except:
                quanity = 1
            #check if first item exist
            #check if first item is in same restaurant as second
            #add item to order or update quanity in specific item
            if len(order.orderitem_set.all())>1:
                if order.orderitem_set.all()[0].items.place==item.place:
                    OrderItem.objects.update_or_create(
                        items=item,
                        order=order,
                        defaults={'quanity':quanity})
                else:
                    messages.error(request,'item is from diffrent restaurant')
            else:
                OrderItem.objects.update_or_create(items=item,
                                                   order=order,
                                                   defaults={'quanity':quanity})
        #remove item from order
        elif "remove-from-order" in data:
            data = data["remove-from-order"]
            item = Item.objects.filter(id=data)[0]
            order_item = OrderItem.objects.filter(items__id=item.id,order__id=order.id).first()
            if order_item.quanity > 1:
                order_item.quanity -= 1
                order_item.save()
            elif order_item.quanity == 1:
                order_item.delete()

        return redirect(f'/restaurant/{pk}')  
    
    order_items = order.orderitem_set.all()

    context = {'items': item_list,
               'order_items':order_items,
               'order':order
               }  
    
    return render(request,'base/restaurant.html',context)

#user orders view
@login_required(login_url="login") 
def orders(request):
    orders = Order.objects.filter(completed=True)
    order_items = OrderItem.objects.filter(order__completed=True)
    print(order_items)
    context = {
        'orders':orders,
        'order_items':order_items
    }
    return render(request,'base/orders.html',context=context)

#account info view
@login_required(login_url="login") 
def account(request):
    return render(request,'base/account.html')

#checkout view with google maps trace
@login_required(login_url="login") 
def checkout(request):
    gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
    order, created = Order.objects.get_or_create(user=request.user,completed=False)
    user_address = UserAdress.objects.filter(pk=1)[0]
    order_items = OrderItem.objects.filter(order__id=order.id)
    restaurant = None
    result_restaurant = None
    result_user = None
    result_city = None
    calculate_distance = 0.0
    calculate_duration = 0.
    #post buttons
    if request.method == "POST":
        data = request.POST
        if 'complete-order' in data:
            data = data["complete-order"]
            order_update = Order.objects.filter(id=int(data)).first()
            order_update.completed = True
            order_update.save()                       
        elif 'remove-from-order' in data:
            data = data["remove-from-order"]
            item = Item.objects.filter(id=data)[0]
            order_item = OrderItem.objects.filter(items__id=item.id,order__id=order.id).first()
            if order_item.quanity > 1:
                order_item.quanity -= 1
                order_item.save()
            elif order_item.quanity == 1:
                order_item.delete()
        return redirect('/checkout/')   
    #order items must exist if we want to initialaze calculations on google maps
    #that shows road on map
    if order_items:
        #check in which restaurant is item
        restaurant = order_items[0].items.place
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
    #calculation delivery price 2 zl per km
    order.delivery_price = round(2*float(calculate_distance),2)
    order.save()
    #calculating copmbined price
    price = 0
    for item in order_items:
        if item:
            price += item.quanity * item.items.price
    order.combined_price = float(price) + order.delivery_price
    order.save()

    context = {
        'order_items':order_items,
        'order':order,
        'restaurant':restaurant,
        'restaurant_location':result_restaurant,
        'city_location':result_city,
        'user_location':result_user,
        'calculate_distance':calculate_distance,
        'calculate_duration':calculate_duration,
        'user_address': user_address
        }
    return render(request,'base/checkout.html',context)

#update address view
@login_required(login_url="login") 
def updateAddress(request):
    address = UserAdress.objects.get(id=1)
    form = AddressForm(instance=address)
    #check logged user with room user if you are allowed to edit this room
    if request.user != address.user: 
        return HTTPResponse('You are not allowed here!')
    if request.method == "POST":
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            return redirect("/checkout/")

    context={'form':form}
    return render(request,'base/update_address.html',context)
