from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length=100)
    scheduled = models.DateTimeField(default=timezone.now)
    content = models.TextField(default="test")
    name_servise = models.CharField(max_length=100, default="Default Service")  
    about_content = models.TextField(default="test")
    image = models.ImageField(upload_to='services', default='services/default0.jpg')
    Edelectus_content_name = models.TextField(default="test")
    Edelectus_content_Description = models.TextField(default="test")
    Temporibus_content_name = models.TextField(default="test")
    Temporibus_content_Description = models.TextField(default="test")
    Feature_content = models.TextField(default="test")
    Description_content_name = models.TextField(default="test")
    Description_content_Description = models.TextField(default="test")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('created_at',)


class ServiceComment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.service.name}'
    
    
class Resume(models.Model):
    NAME = models.CharField(max_length=100, default="test")
    TITLE = models.CharField(max_length=100, default="test")
    SUBJECT = models.CharField(max_length=100, default="test")
    FIRST_TEXT = models.CharField(max_length=100, default="test")
    SECOND_TEXT = models.CharField(max_length=100, default="test")
    THIRD_TEXT = models.CharField(max_length=100, default="test")
    DESCRIPTION = models.TextField(default="test")
    scheduled = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.DESCRIPTION
    
    class Meta:
        ordering = ('created_at',)


class About(models.Model):
    PAGE_NAME = models.CharField(max_length=100, default="test")
    A_LITTLE_ABOUT_US = models.CharField(max_length=100, default="test")
    CREATOR_NAME = models.CharField(max_length=100, default="test")
    ROLE = models.CharField(max_length=100, default="test")
    EMAIL = models.CharField(max_length=100, default="test")
    SERVICES = models.CharField(max_length=100, default="test")
    INTERESTS = models.CharField(max_length=100, default="test")
    ONLINE_PRESENTATION = models.CharField(max_length=100, default="test")
    WORK_HISTORY = models.CharField(max_length=100, default="test")
    DESCRIPTION = models.TextField(default="test")
    scheduled = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.PAGE_NAME
    
    class Meta:
        ordering = ('created_at',)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/icon.png')
    reset_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.user.username




