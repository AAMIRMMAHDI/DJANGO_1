from django.urls import path, include
from .views import *

app_name = 'root' 

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('resume/', resume, name='resume'),
    path('service_details/', service_details, name='service_details'),
    path('contact/', contact_view, name='contact'),  
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('password_reset_code/', password_reset_code, name='password_reset_code'),
    path('password_change/', password_change, name='password_change'),
    path('captcha/', include('captcha.urls')),
    path('Change/', change, name='Change'),
    path('change-icon/', change_profile_icon, name='change_profile_icon'),
    path('save_profile_changes/', save_profile_changes, name='save_profile_changes'),  
    path('services/', services, name='services'),
    path('service_details/<int:service_id>/', service_details, name='service_details'),
]