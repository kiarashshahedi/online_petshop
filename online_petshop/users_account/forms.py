from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.validators import RegexValidator
from .models import Review, Customer, OTP

# Review Form:
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


# Customer Registration Form:
class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email']


# User Creation Form:
class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Login Form:
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
# form for OTP registering
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['mobile', ]


# OTP Form:
class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ['phone_number']


# Verify OTP Form:
class VerifyOTPForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    otp_code = forms.CharField(max_length=6)
