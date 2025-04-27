from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.forms import modelformset_factory
from django.contrib import messages
from django.conf import settings
from mailjet_rest import Client


from django.core import mail
from django.core.mail.message import EmailMessage

from .forms import CustomAuthenticationForm, SignUpForm, AccommodationForm, AccommodationImageForm, AccommodationImageFormSet, ContactSupportForm, LandlordProfileForm

from django.db.models import Prefetch
from .models import CustomUser, Accommodation, AccommodationImage, LandlordProfile, PropertyVerificationDocument
from .forms import PropertyVerificationDocumentForm
from django.core.exceptions import PermissionDenied
import cloudinary.uploader
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

# Home Page
def home(request):
    return render(request, "student/index.html")

@csrf_protect
def landlord_contact(request):
    contact_success = False
    error_message = ''
    if request.method == 'POST':
        form = ContactSupportForm(request.POST)
        if form.is_valid():
            email =   request.POST.get('email')
            subject =   request.POST.get('subject')
            name =   request.POST.get('name')
            message =   request.POST.get('message')

            connection = mail.get_connection()
            connection.open()

            # Send confirmation to user
            user_message = (
                f"Hello {name},\n\n"
                "Thank you for contacting Listins. An Agent will contact you shortly.\n\n"
                "Kind regards,\nListins Services Team"
            )
            mail.EmailMessage(
                subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [email],
                connection=connection
            ).send()

            # Send message to admin/support
            admin_message = (
                f"New landlord contact request:\n\n"
                f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            )
            mail.EmailMessage(
                f"Support Request: {subject}",
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Or your support email
                connection=connection
            ).send()

            connection.close()
            contact_success = True
        else:
            error_message = 'Please correct the errors below.'
    else:
        form = ContactSupportForm()
    
    return render(request, 'landlord/LandlordContact.html', {
        'form': form,
        'contact_success': contact_success,
        'error_message': error_message
    })
    


def studentDetails(request):
    return render(request, "student/viewDetailsStudent.html")


def studentProperties(request):
    return render(request, "student/properties.html")

# def editProperty(request):
#     return render(request, "editProperty.html")

@login_required
def delete_main_image(request, property_id):
    property_obj = get_object_or_404(Accommodation, pk=property_id)
    if request.user != property_obj.landlord:
        raise PermissionDenied
    if property_obj.main_image:
        try:
            public_id = property_obj.main_image.public_id if hasattr(property_obj.main_image, 'public_id') else None
            if public_id:
                cloudinary.uploader.destroy(public_id)
            property_obj.main_image = None
            property_obj.save()
            messages.success(request, "Main image deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete main image: {e}")
    else:
        messages.error(request, "No main image to delete.")
    return redirect('housing:edit_property', property_id=property_id)


@login_required
def view_property(request, property_id):
    property = get_object_or_404(Accommodation, pk=property_id, landlord=request.user)
    existing_images = property.images.all()
    return render(request, 'landlord/viewdetailLandlord.html', {
        'property': property,
        'existing_images': existing_images
    })

@csrf_protect
@login_required
def edit_property(request, property_id):
    property_obj = get_object_or_404(Accommodation, pk=property_id, landlord=request.user)
    

    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES, instance=property_obj)
        image_formset = AccommodationImageFormSet(
            request.POST, request.FILES,
            queryset=AccommodationImage.objects.filter(accommodation=property_obj)
        )
        print("Form errors:", form.errors)
        print("Formset errors:", image_formset.errors)
        if form.is_valid() and image_formset.is_valid():
            form.save()
            for image_form in image_formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.accommodation = property_obj
                    image.save()
            messages.success(request, "Property updated successfully!")
            return redirect('housing:edit_property', property_id=property_obj.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccommodationForm(instance=property_obj)
        image_formset = AccommodationImageFormSet(queryset=AccommodationImage.objects.filter(accommodation=property_obj))

    return render(request, 'landlord/editdetailLandlord.html', {
        'form': form,
        'image_formset': image_formset,
        'property': property_obj,
        'existing_images': AccommodationImage.objects.filter(accommodation=property_obj),
    })

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(AccommodationImage, pk=image_id)
    property_id = image.accommodation.pk
    if request.user == image.accommodation.landlord:
        # Delete from Cloudinary
        try:
            if image.image:
                public_id = image.image.public_id if hasattr(image.image, 'public_id') else None
                if public_id:
                    cloudinary.uploader.destroy(public_id)
            image.delete()
            messages.success(request, "Image deleted successfully.")
        except Exception as e:
            messages.error(request, f"Failed to delete image: {e}")
    else:
        messages.error(request, "You do not have permission to delete this image.")
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

from django.contrib.auth.mixins import LoginRequiredMixin

class LandlordPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'landlord/landlord_password_change.html'
    success_url = reverse_lazy('housing:landlord_profile')

from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def property_verification_upload(request, property_id):
    accommodation = get_object_or_404(Accommodation, pk=property_id, landlord=request.user)
    if request.method == 'POST':
        form = PropertyVerificationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            verification_doc = form.save(commit=False)
            verification_doc.accommodation = accommodation
            verification_doc.status = 'pending'
            verification_doc.save()
            accommodation.is_verified = False  # Explicitly mark as not verified
            accommodation.save()
            messages.success(request, 'Your document was uploaded successfully and is pending review.')
            return render(request, 'landlord/property_verification_upload.html', {
                'form': PropertyVerificationDocumentForm(),
                'success': True,
                'accommodation': accommodation
            })
    else:
        form = PropertyVerificationDocumentForm()
    return render(request, 'landlord/property_verification_upload.html', {
        'form': form,
        'success': False,
        'accommodation': accommodation
    })

@login_required
def landlord_profile(request):
    creating_profile = False
    try:
        profile = LandlordProfile.objects.get(user=request.user)
    except LandlordProfile.DoesNotExist:
        profile = None
        creating_profile = True
    properties = Accommodation.objects.filter(landlord=request.user)

    if request.method == 'POST':
        if profile:
            form = LandlordProfileForm(request.POST, request.FILES, instance=profile)
        else:
            form = LandlordProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            profile = new_profile
            creating_profile = False
    else:
        if profile:
            form = LandlordProfileForm(instance=profile)
        else:
            form = LandlordProfileForm()

    context = {
        'profile': profile,
        'properties': properties,
        'form': form,
        'creating_profile': creating_profile,
    }
    return render(request, 'landlord/LandlordProfile.html', context)


@login_required
def landlord_properties(request):
    # Only show properties where the logged-in user is the landlord
    properties = Accommodation.objects.filter(landlord=request.user)
    return render(request, 'landlord/LandlordProperties.html', {'properties': properties})





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
    return render(request, 'landlord/addProperty.html', {'form': form, 'image_formset': image_formset})











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