from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, ServiceComment
from .forms import ServiceCommentForm, EditCommentForm  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, ContactForm, ProfileIconForm, ServiceCommentForm
from .models import Contact, About, Resume, Service, ServiceComment, UserProfile
import random


# صفحه اصلی
def home(request):
    return render(request, "root/index.html")


# درباره ما
def about(request):
    abouts = About.objects.filter(status=True)
    return render(request, "root/about.html", {"abouts": abouts})


# رزومه
def resume(request):
    resumes = Resume.objects.filter(status=True)
    return render(request, "root/resume.html", {"resumes": resumes})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, ServiceComment
from .forms import ServiceCommentForm

def services(request):
    query = request.GET.get('q')  
    services = Service.objects.filter(name__icontains=query) if query else Service.objects.all()
    return render(request, 'root/services.html', {'services': services})

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

# تغییر اطلاعات پروفایل (فقط برای کاربران لاگین شده)
@login_required
def change_profile_icon(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileIconForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "آیکون پروفایل شما تغییر کرد.")
            return redirect('root:change')
    else:
        form = ProfileIconForm(instance=user_profile)

    return render(request, 'new_Page/change_icon.html', {'form': form})


# صفحه تغییر اطلاعات کاربری
@login_required
def change(request):
    return render(request, "new_Page/Change.html")


# فرم تماس با ما
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
    return render(request, 'root/contact.html', {'form': form, 'approved_contacts': approved_contacts})


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

    return render(request, 'account/signup.html', {'form': form})


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

    return render(request, 'account/login.html', {'form': form})


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

    return render(request, 'account/password_reset_request.html')


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

    return render(request, 'account/password_reset_code.html')


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

        return render(request, 'account/password_change.html', {'form': form})

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
