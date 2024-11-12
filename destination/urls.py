from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('partner_dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('partner_destinations/', views.partner_destinations, name='partner_destinations'),
    path('my_bookings/', views.my_bookings, name='my_bookings'), 
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)