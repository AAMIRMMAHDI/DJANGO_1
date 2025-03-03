from django.db import models

class Statistic(models.Model):
    years_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Statistics: {self.years_experience} Years, {self.projects_completed} Projects, {self.happy_clients} Clients"
    
from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"






from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"پیام از {self.name} - {self.subject}"

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"