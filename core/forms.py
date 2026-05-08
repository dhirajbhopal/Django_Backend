from django import forms
from django.contrib.auth.models import User
from core.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime


# Sign Up Form
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=False, help_text='*', widget=forms.TextInput(attrs={'placeholder': 'username', 'style':'color : red'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'style':'color : red'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'style':'color : red'}))
    
    class Meta:
        model = User
        fields = [
        'username', 
        'first_name', 
        'last_name', 
        'email', 
        'password1', 
        'password2',
        'image',
        'address'
        ]


# Profile Form
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='*', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'style':'color : red'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'style':'color : red'}))
    
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            ]

class ImgForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = User
        fields = [
            'image', 
            ]




