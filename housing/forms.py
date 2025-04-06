from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # This ensures you're using the correct user model

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
        'type': 'email',
        'name': 'email',
        'id': 'email',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter email',
        'maxlength': '100',
        'minlength': '6',
        'required': '',  
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'type': 'password',
        'name': 'password',
        'id': 'password',
        'class': 'block w-full pl-11 pr-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter password',
        'maxlength': '22',
        'minlength': '8',
        'required': '',  
    }))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': '',
        'name': 'name',
        'id': 'name',
        'type': 'text',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter your first name',
        'maxlength': '255',
        'minlength': '3',
    }))
    
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'required': '',
        'name': 'name',
        'id': 'name',
        'type': 'text',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter your last name',
        'maxlength': '255',
        'minlength': '3',
    }))
    
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'required': '',
        'name': 'email',
        'id': 'email',
        'type': 'email',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter your email',
    }))

    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'name': 'phone_number',
        'id': 'phone_number',
        'type': 'tel',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Enter phone number (Optional)',
        'maxlength': '15',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': '',
        'name': 'password1',
        'id': 'password1',
        'type': 'password',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Create a password',
        'maxlength': '22',
        'minlength': '8',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': '',
        'name': 'password2',
        'id': 'password2',
        'type': 'password',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'placeholder': 'Confirm your password',
        'maxlength': '22',
        'minlength': '8',
    }))

    user_type = forms.ChoiceField(choices=User.USER_TYPES, widget=forms.Select(attrs={
        'required': '',
        'name': 'user_type',
        'id': 'user_type',
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
    }))

    class Meta:
        model = User  # Make sure you're using the correct user model
        fields = [ 'first_name', 'last_name', 'username', 'phone_number', 'password1', 'password2', 'user_type']
