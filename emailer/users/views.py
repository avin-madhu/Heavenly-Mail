from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import EmailForm
from django.core.mail import send_mail
from django.conf import settings
from .models import ScheduledEmail
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_email')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        subject = request.POST['subject']
        message = request.POST['message']
        send_on = request.POST.get('send_on', None)
        recipient_email = request.POST['recipient_email']
        time_limit = request.POST.get('time_limit', 365)

        if send_on:
            print('got date to send lol')
            send_on = timezone.datetime.strptime(send_on, "%Y-%m-%dT%H:%M")

        if form.is_valid():
            scheduled_email = form.save(commit=False)
            scheduled_email.user = request.user
            scheduled_email.save()
            if ScheduledEmail.is_ready_to_send:
                send_mail( subject, message, settings.EMAIL_HOST_USER, [recipient_email])
                
                print("email sent")

            ScheduledEmail.objects.create(
                user=request.user,
                subject=subject,
                message=message,
                send_on=send_on,
                time_limit=timezone.timedelta(days=int(time_limit))
            )
            return redirect('email_list')
    else:
        form = EmailForm()
    return render(request, 'create_email.html', {'form': form})

@login_required
def email_list(request):
    emails = ScheduledEmail.objects.filter(user=request.user)
    return render(request,'email_list.html', {'emails':emails})
    
