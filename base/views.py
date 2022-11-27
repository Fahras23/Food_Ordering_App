from django.shortcuts import render, redirect
from .models import Restaurant, Item, Order
from django.http import HttpResponseRedirect
# Create your views here.

def home(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurants':restaurant_list}

    return render(request,'base/home.html',context)
    
def restaurant(request,pk):
    #filtering items for specific restaurant id
    item_list = Item.objects.filter(place__id=pk)
    order = Order.objects.filter(user__username="krzysztof")[0]
    #adding and removing in order with buttons
    if request.method == "POST":
        data = request.POST
        if 'add-to-order' in request.POST:
            data = data['add-to-order']
            item = Item.objects.filter(id=data)[0]
            order = Order.objects.filter(pk=1)[0]
            if order and item:
                #adding items depending on quanity
                order.items.add(item)
                if item.quanity_for_order == 0:
                    item.quanity_for_order += 1
                elif item.quanity_for_order >=1:
                    item.quanity_for_order +=1
                item.save()
                print(item.quanity_for_order)
        
        elif "remove-from-order" in data:
            data = data["remove-from-order"]
            item = Item.objects.filter(id=data)[0]
            order = Order.objects.filter(pk=1)[0]
            if item and order and item.quanity_for_order > 0:
                item.quanity_for_order -= 1
                if item.quanity_for_order == 0:
                    order.items.remove(item)
                item.save()
                
    context = {'items': item_list,'order_items':order.items.all(),'order':order}  
    return render(request,'base/restaurant.html',context)


def orders(request):
    return render(request,'base/orders.html')

def account(request):
    return render(request,'base/account.html')

def checkout(request):
    order = Order.objects.filter(pk=1)[0]
    order_items = order.items.all()
    #delivery 3km for 3 each will add gmaps api
    order.delivery_price = 3*3
    order.save()
    #calculating price for products
    price = 0
    for item in order_items:
        price += item.quanity_for_order * item.price
    order.combined_price = price + order.delivery_price
    order.save()
    context = {'order_items':order_items,'order':order}
    return render(request,'base/checkout.html',context)

"""
#adding to order and removing made with django urls and sending data with link
def add_to_order(request,pk):
    item = Item.objects.filter(id=pk)[0]
    order = Order.objects.filter(pk=1)[0]
    if order and item:
        #adding items depending on quanity
        order.items.add(item)
        if item.quanity_for_order == 0:
            item.quanity_for_order += 1
        elif item.quanity_for_order >=1:
            item.quanity_for_order +=1
        item.save()
        print(item.quanity_for_order)
    
    return HttpResponseRedirect(f'/restaurant/{item.place.id}')

def remove_from_order(request,pk):
    item = Item.objects.filter(id=pk)[0]
    order = Order.objects.filter(pk=1)[0]
    if item and order and item.quanity_for_order > 0:
        item.quanity_for_order -= 1
        if item.quanity_for_order == 0:
            order.items.remove(item)
        item.save()
        
    return HttpResponseRedirect(f'/restaurant/{item.place.id}')
"""
