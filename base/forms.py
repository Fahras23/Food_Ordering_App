from re import L
from django.forms import ModelForm
from .models import UserAdress

class AddressForm(ModelForm):
    class Meta:
        model = UserAdress
        fields = ['street','apartment','city','country','postcode','comments']
