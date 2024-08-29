from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']  # Include role if needed

    def create(self, validated_data):
        # Default role handling
        role = validated_data.get('role', 'patient')  # Default to 'patient'
        user = self.Meta.model(
            email=validated_data['email'],
            username=validated_data['username'],
            role=role
        )
        user.set_password(validated_data['password'])
        user.save()
       
        if role == 'patient':
            PatientProfile.objects.create(user=user)
        elif role == 'doctor':
            DoctorProfile.objects.create(user=user)
        elif role == 'receptionist':
            ReceptionistProfile.objects.create(user=user) 
        return user
       



class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100, read_only=True)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	token = serializers.CharField(max_length=255, read_only=True)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = get_user_model()
        fields = ['token']

from rest_framework import serializers
from .models import DoctorProfile, PatientProfile, ReceptionistProfile, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 
                  'gender', 'date_of_birth', 'phone_number', 'address', 
                    'emergency_contact_name', 'emergency_contact_number', 'role']

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialization', 'bio', 'profile_picture', 
                  'experience', 'qualification']

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientProfile
        fields = ['user', 'medical_history', 'allergies']

class ReceptionistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ReceptionistProfile
        fields = ['user']
