from django.urls import path
from .views import *
from .api_views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # web application views
    path('register/', register, name='register'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('login/', login_view, name='login'), 
    path('password-reset/phone/', phone_number_submit, name='phone_number_submit'),
    path('password-reset/otp/', otp_verification, name='otp_verification'),
    path('password-reset/change/', password_change, name='password_change'),
    path('dashboard/', dashboard, name='dashboard'), 
    path('payment/', payment, name='payment'), 
    path('cricket/', cricket, name='cricket'),
    path('main_details/', main_details, name='main_details'),
    path('sub_details/', sub_details, name='sub_details'), 
    path('verify-phone/', phone_number_verification_view, name='phone_number_verification'),
    path('password-change/<int:user_id>/', phone_number_password_change_view, name='phone_number_password_change'),
    path('send_code/', send_code, name='send_code'),


    # api application api_views
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('api/VerifyOTPView/', VerifyOTPView.as_view(), name='VerifyOTPView'),
    path('api/password-reset/phone/', PhoneNumberSubmitView.as_view(), name='password-reset-phone'),
    path('api/password-reset/otp/', OTPVerificationView.as_view(), name='password-reset-otp'),
    path('api/password-reset/change/', PasswordChangeView.as_view(), name='password-reset-change'),
    path('api/verify-phone/', PhoneNumberVerificationAPIView.as_view(), name='phone_number_verification_api'),
    path('api/password-change/<int:user_id>/', PhoneNumberPasswordChangeAPIView.as_view(), name='phone_number_password_change_api'),
    path('api/title_details/', EventsView.as_view(), name='title_details/'),
    path('api/Sub_details/', SubtitleView.as_view(), name='SubtitleViewSet/'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
