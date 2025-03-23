from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, ServiceComment, About, Resume, Contact, UserProfile
from .forms import ServiceCommentForm, EditCommentForm, SignUpForm, ContactForm, ProfileIconForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
import random

def home(request):
    context = {
        'active_page': 'home'
    }
    return render(request, "root/index.html", context)

def about(request):
    abouts = About.objects.filter(status=True)
    context = {
        'active_page': 'about', 
        'abouts': abouts
    }
    return render(request, "root/about.html", context)

def resume(request):
    resumes = Resume.objects.filter(status=True)
    context = {
        'active_page': 'resume',
        'resumes': resumes
    }
    return render(request, "root/resume.html", context)

# خدمات
def services(request):
    query = request.GET.get('q')  
    services = Service.objects.filter(name__icontains=query) if query else Service.objects.all()
    context = {
        'active_page': 'services',  # شناسه صفحه فعلی
        'services': services
    }
    return render(request, 'root/services.html', context)

def service_details(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    comments = ServiceComment.objects.filter(service=service)
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(ServiceComment, id=comment_id, user=request.user)
            comment.delete()
            return redirect('root:service_details', service_id=service.id)
        elif 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(ServiceComment, id=comment_id, user=request.user)
            form = EditCommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('root:service_details', service_id=service.id)
        else:
            form = ServiceCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.service = service
                comment.user = request.user
                comment.save()
                return redirect('root:service_details', service_id=service.id)
    else:
        form = ServiceCommentForm()
    
    return render(request, 'root/services.html', {
        'service': service,
        'comments': comments,
        'form': form,
    })

# تغییر آیکون پروفایل
@login_required
def change_profile_icon(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileIconForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "آیکون پروفایل شما تغییر کرد.")
            return redirect('root:Change')
    else:
        form = ProfileIconForm(instance=user_profile)

    context = {
        'active_page': 'change',  # شناسه صفحه فعلی
        'form': form
    }
    return render(request, 'new_Page/change_icon.html', context)

# صفحه تغییر اطلاعات کاربری
@login_required
def change(request):
    context = {
        'active_page': 'change'  # شناسه صفحه فعلی
    }
    return render(request, "new_Page/Change.html", context)

# تماس با ما
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
            return redirect('root:contact')
    else:
        form = ContactForm()

    approved_contacts = Contact.objects.filter(is_approved=True)
    context = {
        'active_page': 'contact',  # شناسه صفحه فعلی
        'form': form,
        'approved_contacts': approved_contacts
    }
    return render(request, 'root/contact.html', context)

# ثبت‌نام کاربر جدید
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام موفقیت‌آمیز بود.')
            return redirect('root:home')
    else:
        form = SignUpForm()

    context = {
        'active_page': 'signup',  # شناسه صفحه فعلی
        'form': form
    }
    return render(request, 'account/signup.html', context)

# ورود کاربر
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect('root:home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = AuthenticationForm()

    context = {
        'active_page': 'login',  # شناسه صفحه فعلی
        'form': form
    }
    return render(request, 'account/login.html', context)

# خروج کاربر
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('root:home')

# تولید کد بازیابی رمز عبور
def generate_reset_code():
    return str(random.randint(1000, 9999))

# درخواست بازیابی رمز عبور
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = generate_reset_code()
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            user_profile.reset_code = reset_code
            user_profile.save()
            print(f"کد بازیابی: {reset_code}")
            return redirect('root:password_reset_code')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این ایمیل یافت نشد.')

    context = {
        'active_page': 'password_reset_request'  # شناسه صفحه فعلی
    }
    return render(request, 'account/password_reset_request.html', context)

# بررسی کد بازیابی رمز عبور
def password_reset_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user_profile = UserProfile.objects.get(reset_code=code)
            request.session['user_id'] = user_profile.user.id
            return redirect('root:password_change')
        except UserProfile.DoesNotExist:
            messages.error(request, 'کد وارد شده اشتباه است.')

    context = {
        'active_page': 'password_reset_code'  # شناسه صفحه فعلی
    }
    return render(request, 'account/password_reset_code.html', context)

# تغییر رمز عبور
def password_change(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد. لطفاً دوباره وارد شوید.')
                return redirect('root:login')
        else:
            form = SetPasswordForm(user)

        context = {
            'active_page': 'password_change',  # شناسه صفحه فعلی
            'form': form
        }
        return render(request, 'account/password_change.html', context)

    messages.error(request, 'ابتدا کد بازیابی را وارد کنید.')
    return redirect('root:password_reset_request')

# ذخیره تغییرات اطلاعات کاربری
@login_required
def save_profile_changes(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.save()
        messages.success(request, 'تغییرات با موفقیت ذخیره شدند.')
        return redirect('root:home')

    return redirect('root:change')