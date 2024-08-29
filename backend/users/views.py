from django.shortcuts import render
from users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    EmailVerificationSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    ReceptionistProfileSerializer,  
)
from rest_framework.views import APIView
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
#from .utils import Util
from django.core.mail import send_mail
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

User = get_user_model()

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Set role to 'patient' by default
        data = request.data.copy()
        data['role'] = 'patient'  # Default role
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            if new_user:
                refresh = RefreshToken.for_user(new_user)
                access_token = str(refresh.access_token)
                
                response = Response({
                    'message':'User Registered seccessfully',
                    'user_id':new_user.id,
                    'email':new_user.email,
                    "token": access_token  
                }, status=status.HTTP_201_CREATED)

                # current_site = get_current_site(request)
                # relativeLink = reverse('email-verify')
                # absurl = 'http://' + str(current_site) + relativeLink + "?token=" + str(refresh)
                # email_body = 'Hi ' + new_user.username + ' Use the link below to verify your email \n' + absurl
                
                # send_mail('Verify your email', email_body, "from@example.com", [new_user.email])

                # response = Response(data, status=status.HTTP_201_CREATED)
                
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user is not None:
            # User is authenticated
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email,
                'access_token': access_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWTAuthentication
    permission_classes = [IsAuthenticated]  # Ensure user must be authenticated

    def get(self, request):
        # No need to manually parse the token, JWTAuthentication will handle it
        user = request.user  # This will give you the authenticated user
        print('user', user)

        if not user.is_authenticated:
            raise AuthenticationFailed('User is not authenticated.')

        if user.role == 'doctor':
            print("he is a doctor")
            profile = user.doctor_profile
            serializer = DoctorProfileSerializer(profile)
        elif user.role == 'patient':
            print("he is a patient")
            profile = user.patient_profile
            serializer = PatientProfileSerializer(profile)
        elif user.role == 'receptionist':
            print("he is a doctor")
            profile = user.receptionist_profile
            serializer = ReceptionistProfileSerializer(profile)
        else:
            raise AuthenticationFailed('Invalid user role.')

        return Response(serializer.data)

    

# class UserLogoutViewAPI(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]

#     def get(self, request):
#         refresh_token = request.COOKIES.get('refresh_token', None)
#         access_token = request.COOKIES.get('access_token', None)

#         if refresh_token and access_token:
#             try:
#                 refresh = RefreshToken(refresh_token)
#                 refresh.blacklist()
#                 response = Response()
#                 response.delete_cookie('refresh_token')
#                 response.delete_cookie('access_token')
#                 response.data = {
#                     'message': 'Logged out successfully.'
#                 }
#                 return response
#             except:
#                 response = Response()
#                 response.data = {
#                     'message': 'Something went wrong while logging out.'
#                 }
#                 return response

#         response = Response()
#         response.data = {
#             'message': 'User is already logged out.'
#         }
#         return response