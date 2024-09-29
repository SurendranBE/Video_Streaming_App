from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
# SMS
from django.http import JsonResponse
import random
from .utils import send_verification_code


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            otp = '1111'
            OTPVerification.objects.create(user=user, otp=otp)
            request.session['phone_number'] = user.phone_number
            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


#otp verfication
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        phone_number = request.session.get('phone_number') 
        if not phone_number:
            return render(request, 'verify_otp.html', {'error': 'Phone number not found in session'})
        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            return render(request, 'verify_otp.html', {'error': 'User not found'})
        otp_verification = OTPVerification.objects.filter(user=user, otp=otp).first()
        if not otp_verification:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
        if otp_verification.created_at <= timezone.now() - timedelta(minutes=10):
            return render(request, 'verify_otp.html', {'error': 'OTP expired'})
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if 'phone_number' in request.session:
            del request.session['phone_number']
        return redirect('dashboard')
    return render(request, 'verify_otp.html')

#login page
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

#password change
def phone_number_submit(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                # Normally, you would send an OTP to the user here, but for this example,
                # the OTP is static '2222'
                request.session['phone_number'] = phone_number  # Store phone number in session
                return redirect('otp_verification')
            else:
                messages.error(request, "User with this phone number does not exist.")
    else:
        form = PhoneNumberForm()
    return render(request, 'phone_number.html', {'form': form})

#password change otp verification
def otp_verification(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            phone_number = request.session.get('phone_number')
            if phone_number and otp == '2222':
                return redirect('password_change')
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()
    
    return render(request, 'otp_password_change.html', {'form': form})

#password change
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            
            phone_number = request.session.get('phone_number')
            if not phone_number:
                messages.error(request, "Phone number is not set.")
                return render(request, 'password_change.html', {'form': form})

            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                messages.error(request, "User with this phone number does not exist.")
                return render(request, 'password_change.html', {'form': form})

            user.password = make_password(new_password)
            user.save()

            # Update session auth hash to keep the user logged in after password change
            update_session_auth_hash(request, user)
            
            messages.success(request, "Password reset successfully.")
            return redirect('login')
    else:
        form = PasswordChangeForm()

    return render(request, 'password_change.html', {'form': form})


#Events Details
def dashboard(request):
    return render(request, 'dashboard.html')

def cricket(request):
    event = Events.objects.prefetch_related('subtitles').first()
    return render(request, 'cricket.html', {"event": event})


def main_details(request):
    if request.method == 'POST':
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sub_details')
    else:
        form = EventsForm()
    return render(request, 'title.html', {'form': form})

def sub_details(request):
    if request.method == 'POST':
        form = SubtitleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SubtitleForm()
    return render(request, 'sub_title.html', {'form': form})

# paypal intagration
def payment(request):
    return render(request, "payment.html")


# password change

def phone_number_verification_view(request):
    if request.method == 'POST':
        form = PhoneNumberVerificationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
                return redirect('phone_number_password_change', user_id=user.id)
            except User.DoesNotExist:
                messages.error(request, "User with this phone number does not exist.")
    else:
        form = PhoneNumberVerificationForm()
    
    return render(request, 'phone_number_verification.html', {'form': form})

def phone_number_password_change_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = PhoneNumberPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('login')
            else:
                messages.error(request, "Old password is incorrect.")
    else:
        form = PhoneNumberPasswordChangeForm()
    
    return render(request, 'phone_number_password_change.html', {'form': form})



# SMS SEND OTP FOR PHONE NUMBER

def send_code(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        code = random.randint(1000, 9999)  # Generate a random 4-digit code
        
        try:
            # Send the verification code
            message_sid = send_verification_code(phone_number, code)

            # Update or save the verification code in the user's record
            User.objects.filter(phone_number=phone_number).update(verification_code=code)

            return JsonResponse({'message': 'Verification code sent!', 'sid': message_sid})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'send_code.html')

