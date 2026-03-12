from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, label='Full Name')
    email = forms.EmailField(label='Email Address')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Shipping Address')
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20, label='Postal Code')
    country = forms.CharField(max_length=100, initial='India')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Full Name',
        'class': 'form-input'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-input'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Your message or inquiry...',
        'class': 'form-input',
        'rows': 5
    }))
