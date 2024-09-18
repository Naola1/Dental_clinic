from rest_framework import serializers
from .models import Treatment, TreatmentHistory
from users.models import User

# Serializer for the Treatment model
class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description']

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# Serializer for TreatmentHistory, including nested Treatment, Doctor, and Patient serializers
class TreatmentHistorySerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = TreatmentHistory
        fields = ['id', 'patient', 'doctor', 'treatment', 'treatment_date', 'description', 'follow_up_date']

# Serializer for creating TreatmentHistory records, excludes doctor because it is automatically added from the request
class TreatmentHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentHistory
        fields = ['patient', 'treatment', 'treatment_date', 'description', 'follow_up_date']

    def create(self, validated_data):
        validated_data['doctor'] = self.context['request'].user
        return super().create(validated_data)
    
# Serializer for receptionists to view treatment history, excludes 'description'
class TreatmentHistoryReceptionistSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = TreatmentHistory
        fields = ['id', 'patient', 'doctor', 'treatment', 'treatment_date', 'follow_up_date']