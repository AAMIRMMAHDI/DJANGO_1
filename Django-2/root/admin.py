from django.contrib import admin
from .models import *

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('years_experience', 'projects_completed', 'happy_clients')




from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')


from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')