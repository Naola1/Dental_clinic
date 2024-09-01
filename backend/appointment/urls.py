from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, AvailabilityViewSet, DoctorViewSet, AppointmentBookingViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'availabilities', AvailabilityViewSet, basename='availability')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'bookings', AppointmentBookingViewSet, basename='booking')

# URL patterns
urlpatterns = [
    path('', include(router.urls)), 
]
