from django.contrib import admin
from .models import (
    User, PartnerProfile, Category, Activity, Profile,
    Notification, Destination, DestinationImage, Review,
    Wallet, Booking, AIRecommendation
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_email', 'phone_number', 'joined_date')
    search_fields = ('company_name', 'contact_email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'rating')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birthday', 'gender')
    search_fields = ('user__username', 'location')



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')

    # Action to mark notifications as read
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notifications marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'created_at', 'partner')
    list_filter = ('created_at', 'partner')
    search_fields = ('name', 'location')
    ordering = ('name',)


@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ('destination', 'created_at')
    list_filter = ('created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'destination__name')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'destination', 'booking_date', 'status',
        'total_price', 'payment_status', 'payment_method'
    )
    list_filter = ('status', 'payment_status', 'payment_method', 'booking_date')
    search_fields = ('user__username', 'destination__name')

    # Custom actions to change booking status
    actions = ['mark_as_confirmed', 'mark_as_canceled', 'mark_as_paid']

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"{updated} bookings marked as confirmed.")
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"

    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        self.message_user(request, f"{updated} bookings marked as canceled.")
    mark_as_canceled.short_description = "Mark selected bookings as canceled"

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f"{updated} bookings marked as paid.")
    mark_as_paid.short_description = "Mark selected bookings as paid"


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommended_destination', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'recommended_destination__name')
