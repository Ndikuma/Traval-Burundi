from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('destinations/', views.destinations_view, name='destinations'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('bookings/', views.bookings_view, name='bookings'),
]

# Serve static and media files in development

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)