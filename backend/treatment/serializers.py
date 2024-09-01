from rest_framework import serializers
from .models import Treatment, TreatmentHistory
from users.models import User

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TreatmentHistorySerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = TreatmentHistory
        fields = ['id', 'patient', 'doctor', 'treatment', 'treatment_date', 'description', 'follow_up_date']

class TreatmentHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentHistory
        fields = ['patient', 'treatment', 'treatment_date', 'description', 'follow_up_date']

    def create(self, validated_data):
        # Automatically set the doctor to the current user
        validated_data['doctor'] = self.context['request'].user
        return super().create(validated_data)

class TreatmentHistoryReceptionistSerializer(serializers.ModelSerializer):
    treatment = TreatmentSerializer(read_only=True)
    doctor = UserSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = TreatmentHistory
        fields = ['id', 'patient', 'doctor', 'treatment', 'treatment_date', 'follow_up_date']