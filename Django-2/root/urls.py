from django.urls import path
from .views import home  # ویوی home را ایمپورت کنید

app_name = 'root'  # نام اپ را تعریف کنید

urlpatterns = [
    path('', home, name='home'),  # مسیر اصلی به ویوی home متصل شود
]