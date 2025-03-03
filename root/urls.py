from django.urls import path
from .views import home, contact_view  # مطمئن شوید که ویوها را ایمپورت کرده‌اید

app_name = 'root'  # اگر از فضای نام استفاده می‌کنید

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact_view, name='contact_view'),  # این خط را بررسی کنید
]