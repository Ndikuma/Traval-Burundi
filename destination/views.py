from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Destination, Notification, Profile, Wallet

from .forms import RegistrationForm

def home(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()

            # Create a profile for the user
            profile = Profile.objects.create(user=user)
            profile.save() 

            # Create a wallet for the user
            wallet = Wallet.objects.create(user=user)
            wallet.save() 

            # Log the user in
            login(request, user)

            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to the home page or any page after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})
def user_login(request):
    """
    User login view: Authenticates users using username and password.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'auth/login.html')


@login_required
def user_logout(request):
    """
    User logout view: Logs out the authenticated user.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def destinations_view(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations.html', {'destinations': destinations})

def about_view(request):
    return render(request, 'dasb.html')

def contact_view(request):
    return render(request, 'contact.html')

@login_required
def profile_view(request):
    return render(request, 'auth/profile.html', {'user': request.user})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    # Mark notifications as read
    notifications.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def bookings_view(request):
    bookings = request.user.booking_set.all()  # Assuming User has related bookings
    return render(request, 'bookings.html', {'bookings': bookings})
