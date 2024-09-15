from django.shortcuts import render
from users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    ReceptionistProfileSerializer,
    ChangePasswordSerializer,  
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import DoctorProfile
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        
        data = request.data.copy()
        data['role'] = 'patient' 
        
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
                return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user is not None:
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'username' : user.username,
                'access_token': access_token,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
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
            return Response({'error': 'Invalid user role.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def put(self, request):
        user = request.user
        
        if user.role == 'doctor':
            profile = user.doctor_profile
            serializer = DoctorProfileSerializer(profile, data=request.data, partial=True)
        elif user.role == 'patient':
            profile = user.patient_profile
            serializer = PatientProfileSerializer(profile, data=request.data, partial=True)
        elif user.role == 'receptionist':
            profile = user.receptionist_profile
            serializer = ReceptionistProfileSerializer(profile, data=request.data, partial=True)
        else:
            return Response({'error': 'Invalid user role.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def destroy(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class DoctorListAPIView(ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

class DoctorDetailAPIView(RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer

class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)