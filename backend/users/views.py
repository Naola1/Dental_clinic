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
from .models import DoctorProfile, PatientProfile, ReceptionistProfile
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer

# Get the custom user model
User = get_user_model()

# API view for user registration
class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Set the default role as 'patient' for new users
        data = request.data.copy()
        data['role'] = 'patient' 
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            if new_user:
                # Generate JWT token for the new user
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

# API view for user login    
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny] 

    def post(self, request):
        # Get email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            # If either field is missing, return an error
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)

        if user is not None:
            # Generate JWT token for the authenticated user
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
            # If authentication fails, return an error
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# API view for user profile (based on role)
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the user and determine their role
        user = request.user
        # Fetch and serialize the appropriate profile based on user role
        if user.role == 'doctor':
            try:
                profile = user.doctor_profile
            except DoctorProfile.DoesNotExist:
                return Response({"error": "Doctor profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
            serializer = DoctorProfileSerializer(profile)
        elif user.role == 'patient':
            try:
                profile = user.patient_profile
            except PatientProfile.DoesNotExist:
                return Response({"error": "Patient profile does not exist."}, status=status.HTTP_404_NOT_FOUND)    
            serializer = PatientProfileSerializer(profile)
        elif user.role == 'receptionist':
            try:
               profile = user.receptionist_profile
            except ReceptionistProfile.DoesNotExist:
                return Response({"error": "Receptionist profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReceptionistProfileSerializer(profile)
        else:
            return Response({'error': 'Invalid user role.'}, status=status.HTTP_400_BAD_REQUEST)
        # If the serializer is valid, return the serialized data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        # Update the profile data for each role
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
        # If valid, save and return the updated profile
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def destroy(self, request):
        # Delete the user's account
        user = request.user
        user.delete()
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
# Pagination class for listing results with custom page sizes.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# API view for Getting all list of doctors. 
class DoctorListAPIView(ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

# API view for Getting all detail doctor profiles.
class DoctorDetailAPIView(RetrieveAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'



# API view for changing password.
class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # Handle POST requests to change the user's password.
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        # Validate the serializer data
        if serializer.is_valid():
            user = request.user# Get the authenticated user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)