from django import forms
from .models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your Phone Number'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required")
        return password

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your Phone Number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your Password'}))


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title']

class SubtitleForm(forms.ModelForm):
    class Meta:
        model = Subtitle
        fields = ['content', 'subtitle', 'description', 'video_link', 'image']


# password forget 

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=10)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=4)

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")

        return cleaned_data
    

# password change

class PhoneNumberVerificationForm(forms.Form):
    phone_number = forms.CharField(max_length=15)


class PhoneNumberPasswordChangeForm(forms.Form):    
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        return cleaned_data
