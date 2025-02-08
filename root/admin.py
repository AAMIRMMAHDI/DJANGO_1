from django.contrib import admin
from .models import *


admin.site.register(Service)
admin.site.register(Resume)
admin.site.register(About)
# admin.py
from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email', 'subject')

    def save_model(self, request, obj, form, change):
        if obj.response:  # وقتی پاسخ داده شد
            obj.is_approved = True  # تایید می‌شود
        super().save_model(request, obj, form, change)

admin.site.register(Contact, ContactAdmin)
