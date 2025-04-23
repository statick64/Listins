from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.forms import modelformset_factory
from django.contrib import messages

from .forms import CustomAuthenticationForm, SignUpForm, AccommodationForm, AccommodationImageForm, AccommodationImageFormSet

from django.db.models import Prefetch
from .models import CustomUser, Accommodation, AccommodationImage

# Home Page
def home(request):
    return render(request, "student/index.html")


def studentDetails(request):
    return render(request, "student/viewDetailsStudent.html")


def studentProperties(request):
    return render(request, "student/properties.html")

# def editProperty(request):
#     return render(request, "editProperty.html")

@login_required
def view_property(request, property_id):
    property = get_object_or_404(Accommodation, pk=property_id, landlord=request.user)
    existing_images = property.images.all()
    return render(request, 'landlord/viewdetailLandlord.html', {
        'property': property,
        'existing_images': existing_images
    })

@login_required
def edit_property(request, property_id):
    property_obj = get_object_or_404(Accommodation, pk=property_id, landlord=request.user)
    editing = request.method == 'POST'

    if editing:
        form = AccommodationForm(request.POST, request.FILES, instance=property_obj)
        image_formset = AccommodationImageFormSet(
            request.POST, request.FILES,
            queryset=AccommodationImage.objects.filter(accommodation=property_obj)
        )

        if form.is_valid() and image_formset.is_valid():
            form.save()

            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.accommodation = property_obj
                    image.save()

            return redirect('housing:edit_property', property_id=property_obj.pk)
    else:
        form = AccommodationForm(instance=property_obj)
        image_formset = AccommodationImageFormSet(queryset=AccommodationImage.objects.filter(accommodation=property_obj))

    return render(request, 'landlord/editProperty.html', {
        'form': form,
        'image_formset': image_formset,
        'property': property_obj,
        'existing_images': AccommodationImage.objects.filter(accommodation=property_obj),
        'editing': editing
    })

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(AccommodationImage, pk=image_id)
    property_id = image.accommodation.pk
    if request.user == image.accommodation.landlord:
        image.delete()
    return redirect('housing:edit_property', property_id=property_id)

@login_required
def landlord_home(request):
    if request.user.user_type != 'Landlord':
        # Handle cases where non-landlords access this view
        return render(request, 'error_page.html', {'message': 'You are not authorized to view this page.'})

    accommodations = Accommodation.objects.filter(landlord=request.user).prefetch_related(
        Prefetch(
            'images',
            queryset=AccommodationImage.objects.order_by('pk')[:1],
            to_attr='first_image'
        )
    )
    
    return render(request, "landlord/landlordIndex.html", {'accommodations': accommodations})





@login_required
@csrf_protect
def add_property(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST)
        image_formset = AccommodationImageFormSet(request.POST, request.FILES, queryset=AccommodationImage.objects.none())
        print(form.errors)
        print(image_formset.errors)
        if form.is_valid() and image_formset.is_valid():
            accommodation = form.save(commit=False)
            accommodation.landlord = request.user
            accommodation.save()
            print("New accommodation ID:", accommodation.accommodation_id)
            
            for form in image_formset:
                image = form.save(commit=False)
                image.accommodation = accommodation
                image.save()
            return redirect('housing:landlord_home')    # Or redirect to another page
        
        else:
            return render(request, 'landlord/addProperty.html', {'form': form, 'image_formset': image_formset})
    else:
        form = AccommodationForm()
        image_formset = AccommodationImageFormSet(queryset=AccommodationImage.objects.none())
    return render(request, 'addProperty.html', {'form': form, 'image_formset': image_formset})











@csrf_protect
def user_login(request):  # Renamed to avoid conflict
    if request.method == 'POST':
        form = CustomAuthenticationForm(None, data=request.POST)
        email = request.POST.get('username')
        password = request.POST.get('password')
        print(email, password)
        print(form.errors)


        # Authenticate with email (assuming CustomUser uses email as username)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)  # Use Django’s built-in login function
            print("Login successful")
            if user.user_type == 'Landlord':
                return redirect('housing:landlord_home')  # Replace with actual name
            elif user.user_type == 'Student':
                return redirect('housing:index')  # Replace with actual name 
        else:
            print("Invalid credentials")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login-signup/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('housing:index')





@csrf_protect
def register(request):
    if request.method == 'POST':
        print("pass")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password1'))  # Hash the password
            user.save()
            return redirect('housing:login')  # Redirect after successful registration
        else:
            print(form.errors)  # Debugging: Print errors if the form is invalid
    else:
        form = SignUpForm()
    
    return render(request, 'login-signup/register.html', {'form': form})







# @login_required
# def add_accommodation(request):
#     if request.method == 'POST':
#         accommodation_form = AccommodationForm(request.POST)
#         image_formset = AccommodationImageFormSet(request.POST, request.FILES, prefix='images')
#         if accommodation_form.is_valid() and image_formset.is_valid():
#             accommodation = accommodation_form.save(commit=False)
#             accommodation.landlord = request.user
#             accommodation.save()

#             for form in image_formset:
#                 if form.cleaned_data:
#                     image = form.save(commit=False)
#                     image.accommodation = accommodation
#                     image.save()
#             return redirect('housing:landlord_home')
#         else:
#             return render(request, 'addProperty.html', {'accommodation_form': accommodation_form, 'image_formset': image_formset})
#     else:
#         accommodation_form = AccommodationForm()
#         image_formset = AccommodationImageFormSet(prefix='images')
#     return render(request, 'addProperty.html', {'accommodation_form': accommodation_form, 'image_formset': image_formset})

# @login_required
# def edit_accommodation(request, accommodation_id):
#     accommodation = get_object_or_404(Accommodation, pk=accommodation_id, landlord=request.user)
#     ImageFormSet = forms.modelformset_factory(AccommodationImage, form=AccommodationImageForm, extra=1, can_delete=True)
#     if request.method == 'POST':
#         accommodation_form = AccommodationForm(request.POST, instance=accommodation)
#         image_formset = ImageFormSet(request.POST, request.FILES, instance=accommodation, prefix='images')
#         if accommodation_form.is_valid() and image_formset.is_valid():
#             accommodation = accommodation_form.save()
#             for form in image_formset:
#                 if form.cleaned_data and not form.cleaned_data.get('DELETE'):
#                     image = form.save(commit=False)
#                     image.accommodation = accommodation
#                     image.save()
#                 elif form.cleaned_data and form.cleaned_data.get('DELETE'):
#                     form.instance.delete()
#             return redirect('housing:landlord_home')
#         else:
#             return render(request, 'addProperty.html', {'accommodation_form': accommodation_form, 'image_formset': image_formset})
#     else:
#         accommodation_form = AccommodationForm(instance=accommodation)
#         image_formset = ImageFormSet(instance=accommodation, prefix='images')
#     return render(request, 'addProperty.html', {'accommodation_form': accommodation_form, 'image_formset': image_formset})