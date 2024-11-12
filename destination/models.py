from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal
import locale
from django.db.models import Avg

from django.core.validators import MinValueValidator, MaxValueValidator


locale.setlocale(locale.LC_ALL, '')  # Set the locale for currency formatting

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# Activity Model
class Activity(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.name} at {self.destination.name}"

# User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('partner', 'Partner'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    preferred_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preferred_activities = models.ManyToManyField(Activity, blank=True)

    def is_partner(self):
        return self.role == 'partner'

    def is_customer(self):
        return self.role == 'customer'

    def is_admin(self):
        return self.role == 'admin'
    
class PartnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner_profile')
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='partner_logos/', blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Partner Profile for {self.user.username}"

    
# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='destinations', blank=True)
    partner = models.ForeignKey(User, related_name='destinations', on_delete=models.CASCADE, limit_choices_to={'role': 'partner'})
    def __str__(self):
        return self.name

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, help_text="A short description about the user.")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, help_text="City or location of the user.")
    
    # Additional fields for a more complete profile
    birthday = models.DateField(blank=True, null=True, help_text="User's date of birth.")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number of the user.")
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )
    social_links = models.JSONField(
        blank=True,
        null=True,
        help_text="Social media links in JSON format (e.g., {'facebook': 'url', 'instagram': 'url'})"
    )
    website = models.URLField(blank=True, null=True, help_text="Personal or professional website of the user.")
    interests = models.TextField(blank=True, help_text="User's interests or hobbies.")
    date_joined = models.DateTimeField(default=timezone.now)

    # Methods to get full profile info
    def get_social_links(self):
        return self.social_links if self.social_links else {}

    def __str__(self):
        return f"Profile of {self.user.username}"

    def age(self):
        """Calculate age based on birthday, if provided."""
        if self.birthday:
            today = timezone.now().date()
            return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return None



# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def formatted_message(self):
        return self.message



# Destination Image Model
class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destination_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.destination.name}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Trigger a notification when a new review is posted
        if not self.pk:
            self.create_review_notification()

        super().save(*args, **kwargs)

    def create_review_notification(self):
        message = f"New review posted by {self.user.username} on {self.destination.name}: {self.content}"
        notification = Notification.objects.create(
            user=self.destination.user,
            message=message
        )
        return  notification

    def __str__(self):
        return f"Review by {self.user.username} on {self.destination.name}"


# Wallet Model
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.user.username}"

    def add_funds(self, amount: Decimal):
        self.balance += amount
        self.save()

    def deduct_funds(self, amount: Decimal):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def formatted_balance(self):
        return locale.currency(self.balance, grouping=True)


# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
        ('wallet', 'Wallet Payment'),
        ('online', 'Online Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.destination.price

        if self.payment_method == 'wallet' and self.user.wallet.balance >= self.total_price:
            if not self.user.wallet.deduct_funds(self.total_price):
                raise ValueError("Insufficient balance in wallet")
            self.payment_status = 'paid'
            # Trigger a notification on successful payment
            self.create_payment_notification()

        super().save(*args, **kwargs)

    def create_payment_notification(self):
        message = f"Your booking for {self.destination.name} has been successfully paid and confirmed!"
        notification = Notification.objects.create(
            user=self.user,
            message=message
        )
        return   notification

    def __str__(self):
        return f"Booking by {self.user.username} for {self.destination.name} on {self.booking_date}"


# AI Recommendation Model
class AIRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    recommended_activities = models.ManyToManyField(Activity, blank=True)
    score = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.create_recommendation_notification()

        super().save(*args, **kwargs)

    def create_recommendation_notification(self):
        message = f"We recommend {self.recommended_destination.name} based on your preferences!"
        notification = Notification.objects.create(
            user=self.user,
            message=message
        )
        return notification 

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.recommended_destination.name}"


