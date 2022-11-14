from re import L
from django.forms import ModelForm
from Django_Course_Project.studybud.base.models import Room
from models import Restaurant

class RestaurantForm(ModelForm):
    class Meta:
        model = Room
        fields = 'all'
