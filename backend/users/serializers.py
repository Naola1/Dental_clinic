from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']  

    def create(self, validated_data):
        
        role = validated_data.get('role', 'patient')  
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
        read_only_fields = ['email', 'username']  

    def update(self, instance, validated_data):
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialization', 'bio', 'profile_picture', 
                  'experience', 'qualification']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientProfile
        fields = ['user', 'medical_history', 'allergies']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ReceptionistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ReceptionistProfile
        fields = ['user']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance