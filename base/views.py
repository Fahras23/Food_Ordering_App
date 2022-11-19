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
    context = {'items': item_list,'order_items':order.items.all(),'order':order}
      
    return render(request,'base/restaurant.html',context)

def order(request,pk):
    item = Item.objects.filter(id=pk)[0]
    order = Order.objects.filter(pk=1)[0]
    if order and item:
        order.items.add(item)
    return HttpResponseRedirect(f'/restaurant/{item.place.id}')
    
    

def orders(request):
    return render(request,'base/orders.html')

def account(request):
    return render(request,'base/account.html')