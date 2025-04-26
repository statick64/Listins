from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from .models import Accommodation, AccommodationImage, Booking

User = get_user_model()  # This ensures you're using the correct user model


PROPERTY_TYPE_CHOICES = [
    ('Apartment', 'Apartment'),
    ('Hostel', 'Hostel'),
    ('Single Room', 'Single Room'),
    ('Shared Room', 'Shared Room'),
]

STATUS_CHOICES = [('Available', 'Available'), ('Booked', 'Booked'), ('Coming Soon', 'Coming Soon')]

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






class AccommodationForm(forms.ModelForm):
    property_type = forms.ChoiceField(choices= PROPERTY_TYPE_CHOICES, widget=forms.Select(attrs={
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter price',
        'class': 'block w-full pl-7 border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Title',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))
    
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter address',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter city',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter state',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    bedrooms = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Number of bedrooms',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    bathrooms = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Number of bathrooms',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    square_footage = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Square footage',
        'class': 'mt-1 block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'required': '',
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe the accommodation',
        'class': 'block w-full border-gray-300 focus:border-custom focus:ring-custom',
        'rows': 4,
        'required': '',
    }))
    
    main_image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'hidden file-input',
        'accept': 'image/*'
    }))

    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'block w-full pl-11 !rounded-button border-gray-300 focus:ring-custom focus:border-custom',
        'required': '',
    }))



    class Meta:
        model = Accommodation
        exclude = ['landlord', 'accommodation_id', 'created_at']
        fields = [
            'property_type', 'price', 'address', 'city', 'state',
            'bedrooms', 'bathrooms', 'square_footage',
            'description', 'status', 'title', 'main_image'
        ]
    
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email
    
    
class AccommodationImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'hidden file-input',
        'accept': 'image/*'
    }))
    

    class Meta:
        model = AccommodationImage
        fields = ['image']

AccommodationImageFormSet = forms.modelformset_factory(
    AccommodationImage,
    form=AccommodationImageForm,
    extra=3,  # Number of empty forms to display
    can_delete=True
)





class ContactSupportForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary',
        'name': 'name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your Email',
        'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary',
        'name': 'email'
    }))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary',
        'name': 'subject'
        
        
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Type your message here...',
        'rows': 6,
        'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary',
        'name': 'message'
    }))
