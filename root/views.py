from django.shortcuts import render, redirect
from .models import Statistic, ContactMessage
from .forms import ContactForm

def home(request):
    stats = Statistic.objects.first()  # یا از روش‌های دیگر برای دریافت داده‌ها استفاده کنید
    context = {
        'stats': stats
    }
    return render(request, 'root/index.html', context)

from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # به صفحه اصلی هدایت شود
    else:
        form = ContactForm()
    return render(request, 'root/index.html', {'form': form})