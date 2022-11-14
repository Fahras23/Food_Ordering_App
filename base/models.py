from pydoc import describe
from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    addition_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-addition_date']

    def __str__(self):
        return self.name

class Item(models.Model):
    place = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.name