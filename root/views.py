from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, ContactForm 
from .models import Contact, About, Resume, Service, UserProfile  
import random
from .models import Contact

def home(request):
    return render(request, "root/index.html")

def about(request):
    abouts = About.objects.filter(status=True)
    return render(request, "root/about.html", context={"abouts": abouts})

def resume(request):
    resumes = Resume.objects.filter(status=True)
    return render(request, "root/resume.html", context={"resumes": resumes})

from django.shortcuts import render
from .models import Service

def services(request):
    query = request.GET.get('q')  
    if query:
        services = Service.objects.filter(name__icontains=query) 
    else:
        services = Service.objects.all()  
    return render(request, 'root/services.html', {'services': services})

def service_details(request):
    services = Service.objects.all()
    return render(request, "new Page/service_details.html", context={"services": services})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('root:contact')  
    else:
        form = ContactForm()

    approved_contacts = Contact.objects.filter(is_approved=True)

    return render(request, 'root/contact.html', {
        'form': form,
        'approved_contacts': approved_contacts
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registration was successful and you are logged in.')
            return redirect('root:home')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('root:home')
            else:
                messages.error(request, 'The username or password is incorrect.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('root:home')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
import random

def generate_reset_code():
    return str(random.randint(1000, 9999))

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = generate_reset_code()
            
            # ذخیره کد ریست برای کاربر
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.reset_code = reset_code
            user_profile.save()
            
            # نمایش کد به کنسول برای تست
            print(f"Recovery code: {reset_code}")
            return redirect('root:password_reset_code')
        except User.DoesNotExist:
            messages.error(request, 'User with this email was not found.')
    return render(request, 'account/password_reset_request.html')

def password_reset_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user_profile = UserProfile.objects.get(reset_code=code)
            request.session['user_id'] = user_profile.user.id  # ذخیره شناسه کاربر
            return redirect('root:password_change')
        except UserProfile.DoesNotExist:
            messages.error(request, 'The entered code is incorrect.')
    return render(request, 'account/password_reset_code.html')

def password_change(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password changed successfully. Please log in again.')
                return redirect('root:login')
        else:
            form = SetPasswordForm(user=user)
        return render(request, 'account/password_change.html', {'form': form})
    else:
        messages.error(request, 'Please enter your recovery code first.')
        return redirect('account:password_reset_request')