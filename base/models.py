from pydoc import describe
from django.db import models
from django.contrib.auth.models import User

TYPES_OF_ITEMS = (
       ('food', ('food')),
       ('drink', ('drink')),
   )

TYPES_OF_RESTAURANTS = (
    ('Asian', ('Asian')),
    ('Italian', ('Italian')),
    ('Gregorian', ('Gregorian')),
    ('American', ('American')),
    ('Polish', ('Polish')),
)
VALUES = (
    ('$', (1)),
    ('$$', (2)),
    ('$$$', (3)),
)

# Create your models here.
class UserAdress(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    street = models.CharField(max_length=100,blank=True)
    apartment = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30,blank=True)
    postcode = models.CharField(max_length=30,blank=True)
    comments = models.CharField(max_length=30,blank=True,null=True)
    def __str__(self):
        return f"{self.user} address"

class RestaurantLocation(models.Model):
    street = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30,blank=True)
    postcode = models.CharField(max_length=30,blank=True)
    xmap = models.DecimalField(max_digits=10,decimal_places=4)
    ymap = models.DecimalField(max_digits=10,decimal_places=4)
    
    def __str__(self):
        return self.street

class Restaurant(models.Model):
    location = models.ForeignKey(RestaurantLocation,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    addition_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=32,
        choices=TYPES_OF_RESTAURANTS,
        default='default',
    )
    value=models.CharField(
        max_length=32,
        choices=VALUES,
        default='default',
    )
    class Meta:
        ordering = ['-addition_date']

    def __str__(self):
        return self.name

class Item(models.Model):
    place = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(null=True,blank=True)
    type = models.CharField(
        max_length=32,
        choices=TYPES_OF_ITEMS,
        default='food',
    )
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    combined_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    delivery_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    completed = models.BooleanField(null=True)
    def __str__(self):
        return f'{self.user} order '

class OrderItem(models.Model):
    items = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quanity = models.DecimalField(max_digits=2,decimal_places=0)

    def __str__(self):
        return f"{self.items.name}"
