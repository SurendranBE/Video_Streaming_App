from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import *
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            otp = '1111'  
            OTPVerification.objects.create(user=user, otp=otp)
            request.session['phone_number'] = user.phone_number
            return Response({'message': 'User registered. Please verify OTP.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            phone_number = request.session.get('phone_number')
            if not phone_number:
                return Response({'error': 'Phone number not found in session'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            otp_verification = OTPVerification.objects.filter(user=user, otp=otp).first()
            if not otp_verification:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            if otp_verification.created_at <= timezone.now() - timedelta(minutes=10):
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'phone_number' in request.session:
                del request.session['phone_number']
            return Response({'message': 'OTP verified. User activated.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# forget password  

class PhoneNumberSubmitView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                request.session['phone_number'] = phone_number  # Store phone number in session
                return Response({"detail": "Phone number valid. Proceed to OTP verification."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "User with this phone number does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            phone_number = request.session.get('phone_number')
            if phone_number and otp == '2222':  # Static OTP for simplicity
                return Response({"detail": "OTP verified. Proceed to password change."}, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

User = get_user_model()

class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            phone_number = request.session.get('phone_number')

            if not phone_number:
                return Response({"detail": "Phone number is not set."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({"detail": "User with this phone number does not exist."}, status=status.HTTP_404_NOT_FOUND)

            user.password = make_password(new_password)
            user.save()

            # Optionally: handle user login session or token management

            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# password change
class PhoneNumberVerificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
                return Response({'user_id': user.id}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this phone number does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PhoneNumberPasswordChangeAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhoneNumberPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"success": "Password changed successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# video streaming api


# views.py


class EventsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Event created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        events = Events.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubtitleView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SubtitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Subtitle created successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        subtitles = Subtitle.objects.all()
        serializer = SubtitleSerializer(subtitles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


