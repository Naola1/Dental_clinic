# from rest_framework import serializers
# from .models import Notification

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'message', 'timestamp', 'is_read']
#         read_only_fields = ['user', 'timestamp']

# class FCMDeviceSerializer(serializers.Serializer):
#     registration_id = serializers.CharField(max_length=255)
#     device_type = serializers.ChoiceField(choices=['android', 'ios', 'web']