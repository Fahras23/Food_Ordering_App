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
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
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
    type = models.CharField(
        max_length=32,
        choices=TYPES_OF_ITEMS,
        default='food',
    )
    

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    items = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)
    quanity_for_order = models.DecimalField(max_digits=2,decimal_places=0)
    def __str__(self):
        return self.items.name

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    items = models.ManyToManyField(OrderItem)
    combined_price = models.DecimalField(max_digits=10,decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10,decimal_places=2)
    street = models.TextField(max_length=100)
    city = models.TextField(max_length=100)
 
    def __str__(self):
        return f'{self.user} order nr. {self.id} '