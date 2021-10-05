from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class addresses(forms.ModelForm):
    class Meta:
        model = address
        fields = ('address1','address2','zip_code','country','state')



class regi(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')