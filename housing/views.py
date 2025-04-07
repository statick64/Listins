from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import CustomAuthenticationForm, SignUpForm, AccommodationForm
from .models import CustomUser, Accommodation

# Home Page
def home(request):
    return render(request, "index.html")

@login_required
def landlord_home(request):
    if request.user.user_type != 'Landlord':
        # Handle cases where non-landlords access this view
        return render(request, 'error_page.html', {'message': 'You are not authorized to view this page.'})

    accommodations = Accommodation.objects.filter(landlord=request.user)
    return render(request, "landlordIndex.html", {'accommodations': accommodations})





@login_required
@csrf_protect
def add_property(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.landlord = request.user
            accommodation.save()
            return redirect('housing:landlord_home')  # Or redirect to another page
    else:
        form = AccommodationForm()
    return render(request, 'addProperty.html', {'form': form})





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
    
    return render(request, 'login.html', {'form': form})

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
    
    return render(request, 'register.html', {'form': form})