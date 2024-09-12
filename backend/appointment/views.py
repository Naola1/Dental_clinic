from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment, Availability
from users.models import PatientProfile, User, DoctorProfile
from .serializers import AppointmentSerializer, AvailabilitySerializer, DoctorProfileSerializer, BookingSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from datetime import datetime
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsDoctorOrReceptionistOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'patient' and request.method in ['GET']:
            return True
        elif request.user.role in ['doctor', 'receptionist']:
            return True
        return False


class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctorOrReceptionistOrReadOnly]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['doctor', 'status']
    search_fields = ['patient__first_name', 'patient__last_name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == 'receptionist':
            return Appointment.objects.all()
        if user.role == 'doctor':
            try:
                doctor_profile = DoctorProfile.objects.get(user=user)
                return Appointment.objects.filter(doctor=doctor_profile)
            except DoctorProfile.DoesNotExist:
                return Appointment.objects.none()  
        if user.role == "patient":
            try:
                patient_profile = PatientProfile.objects.get(user=user)
                return Appointment.objects.filter(patient=patient_profile)
            except PatientProfile.DoesNotExist:
                return Appointment.objects.none()  

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().create(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to create appointments."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        print("am in update")
        user = request.user
        print(user)
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update appointments."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'doctor' or user.role == 'receptionist':
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to delete appointments."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'])
    def filter_appointments(self, request):
        doctor_id = request.query_params.get('doctor_id')
        date = request.query_params.get('date')
        speciality = request.query_params.get('speciality')

        queryset = self.get_queryset()

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if date:
            queryset = queryset.filter(appointment_date__date=date)
        if speciality:
            queryset = queryset.filter(doctor__doctor_profile__specialization=speciality)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


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



class AvailabilityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Availability.objects.filter(doctor=user.doctor_profile)
        return Availability.objects.all()


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        doctor = self.get_object()
        availabilities = Availability.objects.filter(doctor=doctor)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)


class AppointmentBookingViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


    @action(detail=True, methods=['post'])
    def book_appointment(self, request, pk=None):
        try:
            doctor = DoctorProfile.objects.get(pk=pk)
            appointment_date_str = request.data.get('appointment_date')
            
            # try:
            appointment_date = datetime.strptime(appointment_date_str, '%d-%m-%Y').date()
            # except ValueError:
            #     return Response({"detail": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}, status=status.HTTP_400_BAD_REQUEST)


            availability = Availability.objects.filter(
                doctor=doctor,
                day_of_week=appointment_date.strftime('%A'),  
            ).first()
        
            if availability:
            
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
