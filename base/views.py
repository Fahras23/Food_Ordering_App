from django.shortcuts import render
from .models import Restaurant, Item
# Create your views here.

def home(request):
    restaurant_list = Restaurant.objects.all()
    context = {'restaurants':restaurant_list}
    return render(request,'base/home.html',context)
    
def restaurant(request,pk):
    #filtering items for specific restaurant id
    item_list = Item.objects.filter(place__id=pk)
    context = {'items': item_list}
    return render(request,'base/restaurant.html',context)

    

def orders(request):
    return render(request,'base/orders.html')

def account(request):
    return render(request,'base/account.html')