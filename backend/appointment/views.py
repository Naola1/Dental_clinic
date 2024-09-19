from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment, Availability
from users.models import PatientProfile, User, DoctorProfile
from .serializers import AppointmentSerializer, AvailabilitySerializer, DoctorProfileSerializer, BookingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from datetime import datetime
from rest_framework.pagination import PageNumberPagination

# Custom pagination class for paginating large result sets.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Custom permission class to restrict access based on user role.
class IsDoctorOrReceptionistOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'patient' and request.method in ['GET']:
            return True
        elif request.user.role in ['doctor', 'receptionist']:
            return True
        return False

# ViewSet for managing Appointment objects
class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctorOrReceptionistOrReadOnly]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['doctor', 'status']
    search_fields = ['patient__first_name', 'patient__last_name']
    pagination_class = StandardResultsSetPagination

    # Customize the queryset based on the user's role
    def get_queryset(self):

        user = self.request.user
        base_queryset = Appointment.objects.filter(status='Scheduled')

        if user.role == 'receptionist':
            return base_queryset
        if user.role == 'doctor':
            try:
                doctor_profile = DoctorProfile.objects.get(user=user)
                return base_queryset.filter(doctor=doctor_profile)
            except DoctorProfile.DoesNotExist:
                return Appointment.objects.none()  
        if user.role == "patient":
            try:
                patient_profile = PatientProfile.objects.get(user=user)
                return base_queryset.filter(patient=patient_profile)
            except PatientProfile.DoesNotExist:
                return Appointment.objects.none()  

    # Only doctors and receptionists are allowed to create appointments
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().create(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to create appointments."}, status=status.HTTP_403_FORBIDDEN)

    # Only doctors and receptionists are allowed to update appointments
    def update(self, request, *args, **kwargs):
        print("am in update")
        user = request.user
        print(user)
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update appointments."}, status=status.HTTP_403_FORBIDDEN)
    
     # Only doctors and receptionists are allowed to delete appointments
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to delete appointments."}, status=status.HTTP_403_FORBIDDEN)

     # Custom action for searching appointments by patient or doctor details
    @action(detail=False, methods=['get'], url_path='search')
    def search_appointments(self, request):
        user = request.user
        search_query = request.query_params.get('query', '')

        if user.role == 'doctor':
           # Allow doctors to search by patient details
            queryset = Appointment.objects.filter(
                patient__user__first_name__icontains=search_query
            ) | Appointment.objects.filter(
                patient__user__last_name__icontains=search_query
            ) | Appointment.objects.filter(
                patient__user__phone_number__icontains=search_query
            )

        elif user.role == 'receptionist':
            # Allow receptionists to search by both patient and doctor details
            queryset = Appointment.objects.filter(
                patient__user__first_name__icontains=search_query
            ) | Appointment.objects.filter(
                patient__user__last_name__icontains=search_query
            ) | Appointment.objects.filter(
                patient__user__phone_number__icontains=search_query
            ) | Appointment.objects.filter(
                doctor__user__first_name__icontains=search_query
            ) | Appointment.objects.filter(
                doctor__user__last_name__icontains=search_query
            ) | Appointment.objects.filter(
                doctor__user__phone_number__icontains=search_query
            )

        else:
            return Response({"detail": "You do not have permission to search appointments."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Action for doctors to change the status of an appointment
    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        user = request.user
        if user.role != 'doctor':
            return Response({"detail": "You do not have permission to change the appointment status."}, status=status.HTTP_403_FORBIDDEN)

        try:
            appointment = self.get_object()
            new_status = request.data.get('status')

            if new_status not in ['Completed', 'Cancelled']:
                return Response({"detail": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

            appointment.status = new_status
            appointment.save()
            return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

# ViewSet for managing doctor availability
class AvailabilityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    pagination_class = StandardResultsSetPagination

    # Doctors can only view their own availability
    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Availability.objects.filter(doctor=user.doctor_profile)
        return Availability.objects.all()

# ViewSet for managing Doctor profiles
class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    pagination_class = StandardResultsSetPagination

    # Custom action for retrieving doctor's availability
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        doctor = self.get_object()
        availabilities = Availability.objects.filter(doctor=doctor)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)

# ViewSet for handling appointment bookings
class AppointmentBookingViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Action to search doctors by specialty and availability
    @action(detail=False, methods=['get'])
    def search_doctors(self, request):
        specialty = request.query_params.get('specialty')
        date = request.query_params.get('date')

        available_doctors = DoctorProfile.objects.filter(specialization=specialty).prefetch_related('availabilities')

        available_doctors_list = []
        for doctor in available_doctors:
            availabilities = doctor.availabilities.filter(day_of_week=date)
            if availabilities.exists():
                available_doctors_list.append({
                    'doctor': DoctorProfileSerializer(doctor).data,
                    'availability': AvailabilitySerializer(availabilities, many=True).data,
                })

        return Response(available_doctors_list)

    # Action to book an appointment with a doctor
    @action(detail=True, methods=['post'])
    def book_appointment(self, request, pk=None):
        try:
            doctor = DoctorProfile.objects.get(pk=pk)
            appointment_date_str = request.data.get('appointment_date')
            
            appointment_date = datetime.strptime(appointment_date_str, '%d-%m-%Y').date()
            availability = Availability.objects.filter(
                doctor=doctor,
                day_of_week=appointment_date.strftime('%A'),  
            ).first()
        
            if availability:
                # Check if the doctor has reached the maximum number of patients for the day
                appointment_count = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date
            ).count()    
                if appointment_count >= availability.max_patients:
                    return Response({"detail": "Doctor has reached the maximum number of patients for the day."}, status=status.HTTP_400_BAD_REQUEST)            
                try:
                    patient_profile = PatientProfile.objects.get(user=request.user)
                except PatientProfile.DoesNotExist:
                    return Response({"detail": "Patient profile not found."}, status=status.HTTP_404_NOT_FOUND)
                appointment_data = {
                    'patient': patient_profile.id,
                    'doctor': doctor.id,
                    'appointment_date': appointment_date,
                    'status': 'Scheduled'
                }
                Booking_serializer = BookingSerializer(data=appointment_data)
                if Booking_serializer.is_valid():
                    appointment = Booking_serializer.save()
                    return Response(AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED)
                return Response(Booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": "Doctor is not available at the requested time."}, status=status.HTTP_400_BAD_REQUEST)
        except DoctorProfile.DoesNotExist:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)