from django.contrib import admin
from .models import Statistic, ContactMessage

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('years_experience', 'projects_completed', 'happy_clients')


from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)