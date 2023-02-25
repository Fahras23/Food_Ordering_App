from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Restaurant)
admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.RestaurantLocation)
admin.site.register(models.UserAdress)