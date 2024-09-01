# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Notification
# from .serializers import NotificationSerializer, FCMDeviceSerializer
# from django.utils import timezone
# from datetime import timedelta
# from appointment.models import Appointment
# from firebase_admin import messaging
# import firebase_admin
# from firebase_admin import credentials


# cred = credentials.Certificate("path/to/your/firebase-adminsdk.json")
# firebase_admin.initialize_app(cred)

# class NotificationViewSet(viewsets.ModelViewSet):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Notification.objects.filter(user=self.request.user)

#     @action(detail=False, methods=['post'])
#     def register_device(self, request):
#         serializer = FCMDeviceSerializer(data=request.data)
#         if serializer.is_valid():
            
#             request.user.fcm_registration_id = serializer.validated_data['registration_id']
#             request.user.save()
#             return Response({'status': 'Device registered'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=False, methods=['post'])
#     def mark_all_read(self, request):
#         Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
#         return Response({'status': 'All notifications marked as read'}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'])
#     def mark_read(self, request, pk=None):
#         notification = self.get_object()
#         notification.is_read = True
#         notification.save()
#         return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)

# def send_appointment_reminders():
#     tomorrow = timezone.now().date() + timedelta(days=1)
#     appointments = Appointment.objects.filter(appointment_date__date=tomorrow)

#     for appointment in appointments:
#         patient = appointment.patient
#         if hasattr(patient, 'fcm_registration_id'):
#             message = messaging.Message(
#                 notification=messaging.Notification(
#                     title='Appointment Reminder',
#                     body=f'You have an appointment tomorrow at {appointment.appointment_date.strftime("%I:%M %p")}',
#                 ),
#                 token=patient.fcm_registration_id,
#             )
            
#             try:
#                 response = messaging.send(message)
#                 print(f'Successfully sent message: {response}')
                
                
#                 Notification.objects.create(
#                     user=patient,
#                     message=f'Reminder: You have an appointment tomorrow at {appointment.appointment_date.strftime("%I:%M %p")}',
#                 )
#             except Exception as e:
#                 print(f'Error sending message to {patient.username}: {e}')

