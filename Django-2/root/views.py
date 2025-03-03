from django.shortcuts import render, redirect
from .models import Statistic, FAQ, ContactMessage
from .forms import ContactForm

def home(request):
    stats = Statistic.objects.first()
    faqs = FAQ.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # ذخیره اطلاعات فرم در دیتابیس
            return redirect('root:home')  # بازگشت به صفحه اصلی بعد از ارسال فرم
    else:
        form = ContactForm()

    context = {
        'stats': stats,
        'faqs': faqs,
        'form': form,
    }
    return render(request, 'root/index.html', context)