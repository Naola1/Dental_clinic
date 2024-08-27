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
from .utils import Util
from django.core.mail import send_mail
import jwt

User = get_user_model()

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        content = {'message': 'Hello!'}
        return Response(content)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            if new_user:
                refresh = RefreshToken.for_user(new_user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                current_site = get_current_site(request)
                relativeLink = reverse('email-verify')
                absurl = 'http://' + str(current_site) + relativeLink + "?token=" + str(refresh)
                email_body = 'Hi ' + new_user.username + ' Use the link below to verify your email \n' + absurl
                
                send_mail('Verify your email', email_body, "from@example.com", [new_user.email])

                response = Response(data, status=status.HTTP_201_CREATED)
                response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)
                response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not password:
            raise AuthenticationFailed('A user password is needed.')

        if not email:
            raise AuthenticationFailed('A user email is needed.')

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed('User not found.')

        if user.is_active:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            response = Response(data)
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
            return response

        return Response({
            'message': 'Something went wrong.'
        })

class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            raise AuthenticationFailed('Unauthenticated user.')

        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_pk = payload['user_id']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise AuthenticationFailed('Invalid token.')

        user_model = get_user_model()
        user = user_model.objects.filter(pk=user_pk).first()

        if user.role == 'doctor':
            profile = user.doctor_profile
            serializer = DoctorProfileSerializer(profile)
        elif user.role == 'patient':
            profile = user.patient_profile
            serializer = PatientProfileSerializer(profile)
        elif user.role == 'receptionist':
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